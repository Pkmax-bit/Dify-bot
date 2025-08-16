'use client'
import { useRouter } from 'next/navigation'
import { useTranslation } from 'react-i18next'
import { useSelectedLayoutSegment } from 'next/navigation'

const WelcomeNav = ({ className }: { className?: string }) => {
  const { t } = useTranslation()
  const router = useRouter()
  const selectedSegment = useSelectedLayoutSegment()
  const activated = selectedSegment === 'welcome'

  const handleClick = () => {
    router.push('/welcome')
  }

  return (
    <div
      className={`${className} ${activated ? 'bg-components-main-nav-nav-button-bg-active text-components-main-nav-nav-button-text-active font-semibold shadow-md' : 'text-components-main-nav-nav-button-text hover:bg-components-main-nav-nav-button-bg-hover'}`}
      onClick={handleClick}
    >
      <div className='flex items-center gap-2'>
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 8h10m0 0V6a2 2 0 00-2-2H9a2 2 0 00-2 2v2m0 0v8a2 2 0 002 2h6a2 2 0 002-2V8" />
        </svg>
        <span className='font-medium'>Xin chào</span>
      </div>
    </div>
  )
}

export default WelcomeNav
