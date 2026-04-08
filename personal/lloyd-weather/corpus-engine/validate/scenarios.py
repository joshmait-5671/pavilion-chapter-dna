"""Test scenarios for validating Lloyd's voice profile."""

SCENARIOS = [
    {
        "id": "routine_daily",
        "name": "Routine daily forecast",
        "question": "What's the weather looking like tomorrow?",
        "context": "Tuesday in March, Westchester NY. High 52, partly cloudy, 10% chance of rain.",
        "tier": "A",
    },
    {
        "id": "snow_event",
        "name": "Big snow event incoming",
        "question": "I'm hearing about a storm this weekend — how bad is it gonna be?",
        "context": "Wednesday asking about Saturday. Models showing 8-14 inches possible for lower Hudson Valley. GFS and Euro disagree on timing by 6 hours.",
        "tier": "C",
    },
    {
        "id": "beach_weekend",
        "name": "Beach weekend decision",
        "question": "We're thinking of going to Montauk this weekend. Saturday or Sunday better?",
        "context": "Thursday asking about weekend. Saturday: 78F, sunny, light wind. Sunday: 74F, 40% chance of afternoon thunderstorms.",
        "tier": "A",
    },
    {
        "id": "models_disagree",
        "name": "Models in disagreement",
        "question": "Is it going to snow Tuesday? I need to decide if I should work from home.",
        "context": "Sunday asking about Tuesday. GFS shows 3-5 inches, Euro shows rain/snow mix with 1 inch. NAM not yet in range.",
        "tier": "B",
    },
    {
        "id": "school_delay",
        "name": "School delay question",
        "question": "Think schools will be delayed tomorrow?",
        "context": "Sunday night. 4-6 inches expected overnight, ending by 6am. Roads should be plowed by 8am but could be icy.",
        "tier": "B",
    },
    {
        "id": "soccer_rainout",
        "name": "Youth sports rain-out",
        "question": "My kid has a soccer game at 2pm Saturday. Think it'll get rained out?",
        "context": "Thursday. Saturday forecast: overcast, 60% chance of showers starting around noon, temps in low 60s.",
        "tier": "A",
    },
    {
        "id": "ski_trip",
        "name": "Ski weekend planning",
        "question": "We're deciding between Hunter and Windham this weekend. Which one's getting more snow?",
        "context": "Wednesday. Storm coming Friday night. Hunter elevation 3,200ft, Windham 3,100ft. Higher elevations favored in this setup.",
        "tier": "B",
    },
    {
        "id": "post_bust",
        "name": "After a forecast miss",
        "question": "Lloyd, you said it was going to dump last night and we got nothing!",
        "context": "Storm tracked 50 miles south of forecast. NYC got 8 inches, Westchester got a dusting.",
        "tier": "C",
    },
    {
        "id": "boring_weather",
        "name": "Nothing interesting happening",
        "question": "Anything exciting weather-wise coming up?",
        "context": "Mid-October. High pressure dominant. 60s and sunny for next 7 days. No storms in extended range.",
        "tier": "A",
    },
    {
        "id": "hurricane_watch",
        "name": "Tropical system approaching",
        "question": "Should I be worried about this hurricane? Do I need to board up the beach house?",
        "context": "Category 1 hurricane in Carolinas tracking northeast. Could impact Jersey Shore as tropical storm in 48 hours. Uncertainty cone is wide.",
        "tier": "C",
    },
]
