'use client'
import { useRouter } from 'next/navigation'
import { useTranslation } from 'react-i18next'

const WelcomeNav = ({ className }: { className?: string }) => {
  const { t } = useTranslation()
  const router = useRouter()

  const handleClick = () => {
    router.push('/welcome')
  }

  return (
    <div
      className={`${className} text-primary-600 hover:bg-primary-50 hover:text-primary-700 border border-transparent`}
      onClick={handleClick}
    >
      Xin chào
    </div>
  )
}

export default WelcomeNav
