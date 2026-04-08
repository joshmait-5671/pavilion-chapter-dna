export type CardType = 'text' | 'icon-text' | 'image-text'

export interface AnswerOption {
  id: string
  text: string
  icon?: string
  image?: string
  imageAlt?: string
}

export interface Question {
  id: string
  number: number
  text: string
  cardType: CardType
  autoAdvance: boolean
  options: AnswerOption[]
}

export interface Chapter {
  id: string
  name: string
  cityPhoto?: string
}

export type Answers = Record<string, string>

export type Screen = 'chapter-select' | 'welcome' | 'survey' | 'loading' | 'card'
