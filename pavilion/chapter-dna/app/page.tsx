'use client'

import { useState, useCallback } from 'react'
import { Chapter, Answers, Screen } from '@/types'
import { calculateArchetype, ArchetypeResult } from '@/lib/archetype'
import { submitToSheets } from '@/lib/submit'
import chaptersData from '@/data/chapters.json'
import questionsData from '@/data/questions.json'

import ChapterSelect from '@/components/ChapterSelect'
import WelcomeScreen from '@/components/WelcomeScreen'
import SurveyQuestion from '@/components/SurveyQuestion'
import ArchetypeLoading from '@/components/ArchetypeLoading'
import ChapterCard from '@/components/ChapterCard'

const chapters: Chapter[] = chaptersData as Chapter[]
const questions = questionsData as import('@/types').Question[]

export default function Home() {
  const [screen, setScreen] = useState<Screen>('chapter-select')
  const [selectedChapter, setSelectedChapter] = useState<Chapter | null>(null)
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [answers, setAnswers] = useState<Answers>({})
  const [animKey, setAnimKey] = useState(0)
  const [result, setResult] = useState<ArchetypeResult | null>(null)

  // Chapter select → Welcome
  const handleChapterSelect = useCallback((chapter: Chapter) => {
    setSelectedChapter(chapter)
    setScreen('welcome')
  }, [])

  // Welcome → Survey
  const handleStart = useCallback(() => {
    setCurrentQuestionIndex(0)
    setAnswers({})
    setAnimKey(k => k + 1)
    setScreen('survey')
  }, [])

  // Record answer
  const handleAnswer = useCallback((questionId: string, optionId: string) => {
    setAnswers(prev => ({ ...prev, [questionId]: optionId }))
  }, [])

  // Advance or complete survey
  const handleNext = useCallback(() => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(i => i + 1)
      setAnimKey(k => k + 1)
    } else {
      // Calculate archetype, submit to Sheets, show loading, then reveal
      setAnswers(prev => {
        const finalAnswers = { ...prev }
        const computed = calculateArchetype(finalAnswers)
        setResult(computed)
        if (selectedChapter) {
          submitToSheets({
            chapter: selectedChapter.name,
            chapterId: selectedChapter.id,
            archetype: computed.archetype.name,
            answers: finalAnswers,
          })
        }
        return finalAnswers
      })
      setScreen('loading')
    }
  }, [currentQuestionIndex])

  // Go back one question (or back to welcome)
  const handleBack = useCallback(() => {
    if (currentQuestionIndex === 0) {
      setScreen('welcome')
    } else {
      setCurrentQuestionIndex(i => i - 1)
      setAnimKey(k => k + 1)
    }
  }, [currentQuestionIndex])

  // Loading → Card reveal
  const handleLoadingComplete = useCallback(() => {
    setScreen('card')
  }, [])

  // Restart
  const handleRestart = useCallback(() => {
    setSelectedChapter(null)
    setAnswers({})
    setCurrentQuestionIndex(0)
    setResult(null)
    setScreen('chapter-select')
  }, [])

  // ── Render ──────────────────────────────────────────────────

  if (screen === 'chapter-select') {
    return <ChapterSelect chapters={chapters} onSelect={handleChapterSelect} />
  }

  if (screen === 'welcome' && selectedChapter) {
    return (
      <WelcomeScreen
        chapterName={selectedChapter.name}
        onStart={handleStart}
      />
    )
  }

  if (screen === 'survey' && selectedChapter) {
    const question = questions[currentQuestionIndex]
    if (!question) return null
    return (
      <SurveyQuestion
        key={question.id}
        question={question}
        questionIndex={currentQuestionIndex}
        totalQuestions={questions.length}
        answers={answers}
        chapterName={selectedChapter.name}
        onAnswer={handleAnswer}
        onNext={handleNext}
        onBack={handleBack}
        isFirst={currentQuestionIndex === 0}
        isLast={currentQuestionIndex === questions.length - 1}
        animKey={animKey}
      />
    )
  }

  if (screen === 'loading' && selectedChapter) {
    return (
      <ArchetypeLoading
        chapterName={selectedChapter.name}
        onComplete={handleLoadingComplete}
      />
    )
  }

  if (screen === 'card' && selectedChapter && result) {
    return (
      <ChapterCard
        result={result}
        chapter={selectedChapter}
        onRestart={handleRestart}
      />
    )
  }

  return null
}
