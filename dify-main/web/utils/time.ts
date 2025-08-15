import dayjs, { type ConfigType } from 'dayjs'
import utc from 'dayjs/plugin/utc'
import timezone from 'dayjs/plugin/timezone'

dayjs.extend(utc)
dayjs.extend(timezone)

// Set default timezone to Vietnam
dayjs.tz.setDefault('Asia/Ho_Chi_Minh')

export const isAfter = (date: ConfigType, compare: ConfigType) => {
  return dayjs(date).isAfter(dayjs(compare))
}

export const formatTime = ({ date, dateFormat }: { date: ConfigType; dateFormat: string }) => {
  return dayjs(date).tz('Asia/Ho_Chi_Minh').format(dateFormat)
}
