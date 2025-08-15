'use client'
import React from 'react'
import Link from 'next/link'

const TikTokNav = () => {
  return (
    <Link 
      href="/tiktok" 
      className="relative group flex items-center space-x-1 px-3 py-2 text-sm font-medium text-gray-700 hover:text-pink-600 transition-all duration-200 rounded-md hover:bg-pink-50"
    >
      {/* TikTok Icon */}
      <svg 
        className="w-5 h-5 group-hover:scale-110 transition-transform" 
        viewBox="0 0 24 24" 
        fill="currentColor"
      >
        <path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-5.2 1.74 2.89 2.89 0 012.31-4.64 2.93 2.93 0 01.88.13V9.4a6.84 6.84 0 00-.88-.05A6.33 6.33 0 005 20.1a6.34 6.34 0 0010.86-4.43v-7a8.16 8.16 0 004.77 1.52v-3.4a4.85 4.85 0 01-1-.1z"/>
      </svg>
      
      <span className="hidden sm:inline">TikTok</span>
      
      {/* Pulse animation indicator */}
      <div className="absolute -top-1 -right-1 w-2 h-2 bg-pink-500 rounded-full animate-pulse"></div>
    </Link>
  )
}

export default TikTokNav
