'use client'
import React, { useState, useCallback } from 'react'
import Link from 'next/link'
import { useTranslation } from 'react-i18next'

type FacebookNavProps = {
  className?: string
}

const FacebookNav = ({ className }: FacebookNavProps) => {
  const { t } = useTranslation()
  const [showToast, setShowToast] = useState(false)

  const handleClick = useCallback(() => {
    setShowToast(true)
    setTimeout(() => {
      setShowToast(false)
    }, 3000)
  }, [])

  return (
    <>
      <Link 
        href="/facebook"
        className={`${className} bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white transition-all duration-200 hover:shadow-md`}
        onClick={handleClick}
      >
        <svg className="w-4 h-4 mr-1.5" fill="currentColor" viewBox="0 0 24 24">
          <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
        </svg>
        Facebook
      </Link>
      
      {showToast && (
        <div className="fixed top-4 right-4 z-50 animate-slide-in-from-top">
          <div className="bg-blue-500 text-white px-4 py-3 rounded-lg shadow-lg max-w-md">
            <div className="flex items-center">
              <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span className="text-sm font-medium">
                📱 Chào mừng đến với Facebook Reels! Khám phá những video AI thú vị!
              </span>
            </div>
          </div>
        </div>
      )}
    </>
  )
}

export default FacebookNav
