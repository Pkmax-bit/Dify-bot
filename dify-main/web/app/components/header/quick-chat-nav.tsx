'use client'
import Link from 'next/link'
import { useSelectedLayoutSegment } from 'next/navigation'
import { useTranslation } from 'react-i18next'

type Props = {
  className?: string
}

const QuickChatNav = ({
  className,
}: Props) => {
  const { t } = useTranslation()
  const selectedSegment = useSelectedLayoutSegment()
  const activated = selectedSegment === 'quick-chat' || selectedSegment === 'quick-chat-v2' || selectedSegment === 'quick-chat-v3'

  return (
    <Link href="/quick-chat-v2" className={`
      ${className}
      ${activated ? 'bg-primary-100 text-primary-600' : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'}
    `}>
      <div className='flex items-center gap-2'>
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
        </svg>
        <span className='font-medium'>Quick Chat V2</span>
      </div>
    </Link>
  )
}

export default QuickChatNav
