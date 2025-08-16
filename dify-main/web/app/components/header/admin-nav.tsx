'use client'
import { useCallback } from 'react'
import { useTranslation } from 'react-i18next'
import { useSelectedLayoutSegment } from 'next/navigation'
import { useRouter } from 'next/navigation'
import {
  RiSettingsLine,
  RiDashboardLine,
} from '@remixicon/react'

type Props = {
  className?: string
}

const AdminNav = ({
  className,
}: Props) => {
  const { t } = useTranslation()
  const router = useRouter()
  const selectedSegment = useSelectedLayoutSegment()
  const activated = selectedSegment === 'admin'

  const handleOpenDashboard = useCallback(() => {
    router.push('/admin')
  }, [router])

  return (
    <button 
      onClick={handleOpenDashboard}
      className={`
        ${className}
        ${activated ? 'bg-primary-100 text-primary-600' : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'}
      `}
    >
      <div className='flex items-center gap-2'>
        <RiDashboardLine className="w-4 h-4" />
        <span className='font-medium'>Admin Dashboard</span>
      </div>
    </button>
  )
}

export default AdminNav
