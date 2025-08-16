import React from 'react'

interface ScrollAreaProps {
  className?: string
  children: React.ReactNode
}

export const ScrollArea: React.FC<ScrollAreaProps> = ({ className = '', children }) => {
  return (
    <div className={`relative overflow-hidden ${className}`}>
      <div className="h-full w-full overflow-auto">
        {children}
      </div>
    </div>
  )
}
