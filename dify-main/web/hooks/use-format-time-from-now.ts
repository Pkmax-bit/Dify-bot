import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import timezone from 'dayjs/plugin/timezone'
import utc from 'dayjs/plugin/utc'
import { useCallback } from 'react'
import { useI18N } from '@/context/i18n'
import 'dayjs/locale/zh-cn'
import 'dayjs/locale/vi'

dayjs.extend(relativeTime)
dayjs.extend(timezone)
dayjs.extend(utc)

export const useFormatTimeFromNow = () => {
  const { locale } = useI18N()
  const formatTimeFromNow = useCallback((time: number) => {
    let dayjsLocale = locale
    if (locale === 'zh-Hans') {
      dayjsLocale = 'zh-cn'
    } else if (locale === 'vi-VN') {
      dayjsLocale = 'vi'
    }
    
    return dayjs(time).tz('Asia/Ho_Chi_Minh').locale(dayjsLocale).fromNow()
  }, [locale])

  return { formatTimeFromNow }
}
