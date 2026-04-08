'use client'

import { useState, useEffect } from 'react'
import { Question, Answers } from '@/types'
import AnswerCard from './AnswerCard'
import ProgressBar from './ProgressBar'

interface SurveyQuestionProps {
  question: Question
  questionIndex: number
  totalQuestions: number
  answers: Answers
  chapterName: string
  onAnswer: (questionId: string, optionId: string) => void
  onNext: () => void
  onBack: () => void
  isFirst: boolean
  isLast: boolean
  animKey: number
}

export default function SurveyQuestion({
  question,
  questionIndex,
  totalQuestions,
  answers,
  chapterName,
  onAnswer,
  onNext,
  onBack,
  isFirst,
  isLast,
  animKey,
}: SurveyQuestionProps) {
  const selectedId = answers[question.id]
  const [isAdvancing, setIsAdvancing] = useState(false)

  // Reset advancing state when question changes
  useEffect(() => {
    setIsAdvancing(false)
  }, [question.id])

  const handleSelect = (optionId: string) => {
    if (isAdvancing) return
    onAnswer(question.id, optionId)

    if (question.autoAdvance) {
      setIsAdvancing(true)
      setTimeout(() => {
        onNext()
      }, 360)
    }
  }

  const isImageGrid = question.cardType === 'image-text'

  return (
    <div className="flex flex-col min-h-dvh bg-[#180A5C]">
      {/* Progress bar */}
      <ProgressBar current={questionIndex + 1} total={totalQuestions} />

      {/* Header */}
      <div className="flex items-center justify-between px-5 pt-5 pb-0">
        <button
          onClick={onBack}
          className={`
            flex items-center gap-1.5 text-[13px] text-white/40 hover:text-white/70
            transition-colors duration-150 -ml-1 py-1 px-1
            ${isFirst ? 'invisible' : ''}
          `}
        >
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M10 12L6 8L10 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
          Back
        </button>

        <p className="text-[12px] font-medium tracking-wider text-pav-purple-400/60 uppercase">
          {questionIndex + 1} / {totalQuestions}
        </p>

        <p className="text-[12px] text-white/30 max-w-[100px] truncate text-right">
          {chapterName}
        </p>
      </div>

      {/* Question text */}
      <div
        key={animKey}
        className="px-5 pt-6 pb-5 animate-slide-in"
      >
        <h2 className="text-[24px] sm:text-[28px] font-display font-bold text-white leading-[1.2] tracking-tight">
          {question.text}
        </h2>
      </div>

      {/* Answer grid */}
      <div
        key={`grid-${animKey}`}
        className={`
          px-5 animate-slide-in
          ${isImageGrid
            ? 'grid grid-cols-2 gap-2.5'
            : 'grid grid-cols-2 gap-2.5'
          }
        `}
        style={{ animationDelay: '40ms' }}
      >
        {question.options.map((option) => (
          <AnswerCard
            key={option.id}
            option={option}
            cardType={question.cardType}
            isSelected={selectedId === option.id}
            isDisabled={isAdvancing}
            onSelect={() => handleSelect(option.id)}
          />
        ))}
      </div>

      {/* Manual next button — only on last question */}
      {isLast && (
        <div
          className={`
            px-5 mt-5 transition-all duration-300
            ${selectedId ? 'opacity-100' : 'opacity-0 pointer-events-none'}
          `}
        >
          <button
            onClick={onNext}
            disabled={!selectedId}
            className="w-full py-4 bg-pav-pink text-white font-semibold text-[15px] rounded-xl
                       hover:bg-pav-pink-800 active:scale-[0.98] transition-all duration-150 disabled:opacity-40"
          >
            Submit
          </button>
        </div>
      )}

      {/* Spacer */}
      <div className="flex-1 min-h-8" />
    </div>
  )
}
