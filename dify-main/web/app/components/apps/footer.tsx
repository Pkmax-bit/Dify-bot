import React from 'react'
import Link from 'next/link'
import { RiDiscordFill, RiGithubFill } from '@remixicon/react'
import { useTranslation } from 'react-i18next'

type CustomLinkProps = {
  href: string
  children: React.ReactNode
}

const CustomLink = React.memo(({
  href,
  children,
}: CustomLinkProps) => {
  return (
    <Link
      className='flex h-8 w-8 cursor-pointer items-center justify-center transition-opacity duration-200 ease-in-out hover:opacity-80'
      target='_blank'
      rel='noopener noreferrer'
      href={href}
    >
      {children}
    </Link>
  )
})

const Footer = () => {
  const { t } = useTranslation()

  return (
    <footer className='relative shrink-0 grow-0 px-12 py-2'>
      <h3 className='text-gradient text-xl font-semibold leading-tight'>{t('app.join')}</h3>
      <p className='system-sm-regular mt-1 text-text-tertiary'>{t('app.communityIntro')}</p>
      
    </footer>
  )
}

export default React.memo(Footer)
