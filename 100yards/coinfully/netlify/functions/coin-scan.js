const Anthropic = require('@anthropic-ai/sdk');
const { Resend } = require('resend');

const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
const resend = new Resend(process.env.RESEND_API_KEY);

const TEAM_EMAIL = process.env.TEAM_EMAIL || 'wyatt@coinfully.com';

const WYATT_SYSTEM_PROMPT = `You are Wyatt McDonald, President of Coinfully — a professional numismatist who buys coin collections from inheritors and investors across the country. Someone just sent you a photo of a coin asking what it is and what it might be worth.

Your job: give them a genuine, useful answer. Not a pitch. Not a form letter.

How you write:
- Specific when the photo allows ("This looks like a 1921-D Morgan Dollar" not "this appears to be a silver coin")
- Honest about what you can and can't tell from a photo alone — condition, grade, and mint marks matter and sometimes the photo doesn't show them clearly
- Give a realistic value range where you can, with a caveat that it depends on grade and condition
- If you can't identify it from the photo, say so directly and ask for a clearer photo or the other side
- 3-4 short paragraphs — like a real email, not a report
- End with a genuine, low-pressure offer: if they want a real appraisal, you're happy to take a look at the full collection
- Never promise a specific offer price from just a photo
- Sign off as: Wyatt McDonald, Coinfully

Tone examples:
"Looks like a 1921 Morgan Dollar to me — one of the most common dates, but still a nice coin. In circulated condition they typically run $25–40. If it grades out better than it looks here, that changes. Happy to take a closer look if you've got more."

"Hard to tell from this angle — can you send me the reverse side? The date and mint mark will tell me a lot. At first glance it could be a Walking Liberty Half Dollar, which would be worth a look."`;

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method not allowed' };
  }

  try {
    const { email, imageBase64, imageType } = JSON.parse(event.body);

    if (!email || !imageBase64) {
      return { statusCode: 400, body: JSON.stringify({ error: 'Missing email or image' }) };
    }

    // 1. Get AI assessment in Wyatt's voice
    const message = await anthropic.messages.create({
      model: 'claude-opus-4-5',
      max_tokens: 600,
      system: WYATT_SYSTEM_PROMPT,
      messages: [{
        role: 'user',
        content: [
          {
            type: 'image',
            source: { type: 'base64', media_type: imageType || 'image/jpeg', data: imageBase64 }
          },
          {
            type: 'text',
            text: "Here's a photo of my coin. Can you tell me what it is and what it might be worth?"
          }
        ]
      }]
    });

    const draft = message.content[0].text;

    // 2. Send customer: warm acknowledgment only — no AI content
    try {
      await resend.emails.send({
        from: 'Coinfully <onboarding@resend.dev>',
        to: email,
        subject: 'Got your coin — we\'ll be back within 24 hours',
        html: `
          <div style="font-family: Georgia, serif; max-width: 520px; margin: 0 auto; padding: 40px 24px; color: #1a1a1a; line-height: 1.75;">
            <img src="https://coinfully-homepage.netlify.app/assets/logo-coinfully-dark.png" alt="Coinfully" style="height: 26px; margin-bottom: 36px; display: block; filter: invert(1);">
            <p style="margin: 0 0 16px;">Got your photo — thanks for sending it over.</p>
            <p style="margin: 0 0 16px;">I'll take a look and send you a proper read within 24 hours. If you have more coins or want to share the other side, just reply here and attach whatever you've got.</p>
            <p style="margin: 0 0 32px;">Talk soon,<br><strong>Wyatt McDonald</strong><br><span style="color: #888; font-size: 14px;">Coinfully · Charlotte, NC</span></p>
            <hr style="border: none; border-top: 1px solid #eee; margin: 0 0 24px;">
            <p style="font-size: 12px; color: #aaa; margin: 0;">704-621-4893 · coinfully.com</p>
          </div>
        `
      });
    } catch (emailErr) {
      console.warn('Customer acknowledgment email failed:', emailErr.message);
    }

    // 3. Send team: coin photo + AI draft + one-click mailto reply button
    const mailtoSubject = encodeURIComponent("Your coin — a quick read from Wyatt");
    const mailtoBody = encodeURIComponent(draft);
    const mailtoLink = `mailto:${email}?subject=${mailtoSubject}&body=${mailtoBody}`;

    // Format draft as HTML paragraphs
    const draftHtml = draft
      .split('\n')
      .filter(p => p.trim())
      .map(p => `<p style="margin:0 0 14px;line-height:1.7;">${p}</p>`)
      .join('');

    await resend.emails.send({
      from: 'Coin Scanner <onboarding@resend.dev>',
      to: TEAM_EMAIL,
      subject: `🪙 New coin scan — ${email}`,
      attachments: [{
        filename: 'coin-submission.jpg',
        content: imageBase64,
        encoding: 'base64'
      }],
      html: `
        <div style="font-family: -apple-system, sans-serif; max-width: 600px; margin: 0 auto; padding: 32px 24px; color: #1a1a1a;">

          <div style="background: #f5f5f0; border-radius: 10px; padding: 20px 24px; margin-bottom: 28px;">
            <p style="margin: 0 0 4px; font-size: 12px; color: #888; text-transform: uppercase; letter-spacing: 0.05em;">New submission</p>
            <p style="margin: 0; font-size: 18px; font-weight: 700;">${email}</p>
          </div>

          <p style="margin: 0 0 8px; font-size: 13px; font-weight: 600; color: #888; text-transform: uppercase; letter-spacing: 0.05em;">Coin photo</p>
          <img src="cid:coin-submission.jpg" alt="Submitted coin" style="width:100%;max-width:480px;border-radius:10px;margin-bottom:28px;display:block;">

          <p style="margin: 0 0 8px; font-size: 13px; font-weight: 600; color: #888; text-transform: uppercase; letter-spacing: 0.05em;">AI draft — in your voice</p>
          <div style="background: #fffdf5; border: 2px solid #F5C342; border-radius: 10px; padding: 20px 24px; margin-bottom: 24px; font-family: Georgia, serif;">
            ${draftHtml}
          </div>

          <a href="${mailtoLink}"
             style="display:inline-block; background:#F5C342; color:#0a0a0a; font-weight:700; font-size:15px; text-decoration:none; padding:14px 28px; border-radius:8px; margin-bottom:12px;">
            Send this draft →
          </a>

          <p style="margin: 0; font-size: 12px; color: #aaa;">Clicking opens your email client pre-addressed to ${email} with the draft ready to review and send.</p>

        </div>
      `
    });

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ok: true })
    };

  } catch (err) {
    console.error('coin-scan error:', err);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Something went wrong. Please try again.' })
    };
  }
};
