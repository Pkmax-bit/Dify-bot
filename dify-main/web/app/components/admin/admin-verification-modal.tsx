'use client'

import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { RiCloseLine, RiMailLine, RiShieldCheckLine } from '@remixicon/react'
import Button from '@/app/components/base/button'
import Modal from '@/app/components/base/modal'
import Toast from '@/app/components/base/toast'

type AdminVerificationModalProps = {
  isShow: boolean
  onClose: () => void
  onSuccess: () => void
}

const AdminVerificationModal = ({ isShow, onClose, onSuccess }: AdminVerificationModalProps) => {
  const { t } = useTranslation()
  const [code, setCode] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [timeLeft, setTimeLeft] = useState(0)
  const [codeSent, setCodeSent] = useState(false)
  const [sessionId, setSessionId] = useState('')

  // Auto send verification code when modal opens
  const sendVerificationCode = async () => {
    setIsLoading(true)
    try {
      // Generate session ID
      const newSessionId = Math.random().toString(36).substring(2) + Date.now().toString(36)
      setSessionId(newSessionId)
      
      const response = await fetch('/console/api/admin/send-verification', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-session-id': newSessionId,
        },
        body: JSON.stringify({}), // No email needed, use configured email
      })

      if (response.ok) {
        setCodeSent(true)
        setTimeLeft(300) // 5 minutes countdown
        const countdown = setInterval(() => {
          setTimeLeft((prev) => {
            if (prev <= 1) {
              clearInterval(countdown)
              return 0
            }
            return prev - 1
          })
        }, 1000)
        Toast.notify({ type: 'success', message: 'Mã xác minh đã được gửi đến email của admin' })
      } else {
        const error = await response.json()
        Toast.notify({ type: 'error', message: error.message || 'Không thể gửi mã xác minh' })
      }
    } catch (error) {
      Toast.notify({ type: 'error', message: 'Lỗi kết nối. Vui lòng thử lại.' })
    } finally {
      setIsLoading(false)
    }
  }

  // Auto send code when modal opens
  React.useEffect(() => {
    if (isShow && !codeSent) {
      sendVerificationCode()
    }
  }, [isShow, codeSent])

  const verifyCode = async () => {
    if (!code) {
      Toast.notify({ type: 'error', message: 'Vui lòng nhập mã xác minh' })
      return
    }

    setIsLoading(true)
    try {
      const response = await fetch('/console/api/admin/verify-code', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code, session_id: sessionId }),
      })

      if (response.ok) {
        Toast.notify({ type: 'success', message: 'Xác minh thành công!' })
        // Set session token for admin access in both localStorage and cookies
        const data = await response.json()
        localStorage.setItem('admin_session_token', data.token)
        localStorage.setItem('admin_session_expires', (Date.now() + (60 * 60 * 1000)).toString()) // 1 hour
        localStorage.setItem('admin_session_id', sessionId)
        
        // Set cookies for middleware
        document.cookie = `admin_session_token=${data.token}; max-age=3600; path=/`
        document.cookie = `admin_session_expires=${Date.now() + (60 * 60 * 1000)}; max-age=3600; path=/`
        document.cookie = `admin_session_id=${sessionId}; max-age=3600; path=/`
        
        onSuccess()
        onClose()
      } else {
        const error = await response.json()
        Toast.notify({ type: 'error', message: error.message || 'Mã xác minh không đúng' })
      }
    } catch (error) {
      Toast.notify({ type: 'error', message: 'Lỗi kết nối. Vui lòng thử lại.' })
    } finally {
      setIsLoading(false)
    }
  }

  const formatTime = (seconds: number) => {
    const minutes = Math.floor(seconds / 60)
    const remainingSeconds = seconds % 60
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
  }

  const handleClose = () => {
    setCode('')
    setTimeLeft(0)
    setCodeSent(false)
    setSessionId('')
    onClose()
  }

  const handleResendCode = () => {
    setCodeSent(false)
    sendVerificationCode()
  }

  return (
    <Modal
      isShow={isShow}
      onClose={handleClose}
      className="!max-w-lg !w-full"
    >
      <div className="bg-gradient-to-br from-sky-50 via-white to-emerald-50 p-8 rounded-2xl border-2 border-sky-200 shadow-2xl">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-4">
            <div className="flex items-center justify-center w-16 h-16 bg-gradient-to-br from-sky-100 to-blue-100 rounded-2xl shadow-lg border-2 border-sky-300">
              <RiShieldCheckLine className="w-8 h-8 text-sky-600" />
            </div>
            <div>
              <h3 className="text-2xl font-bold text-gray-700 mb-1">
                🔐 Xác minh Admin
              </h3>
              <p className="text-base text-gray-600 font-medium">
                Truy cập Dashboard Quản lý
              </p>
            </div>
          </div>
          <button
            onClick={handleClose}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors border-2 border-gray-200 hover:border-gray-300 shadow-sm"
          >
            <RiCloseLine className="w-6 h-6 text-gray-500 hover:text-gray-700" />
          </button>
        </div>

        {!codeSent ? (
          <div className="space-y-6">
            <div className="text-center bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-xl border-2 border-blue-200">
              <div className="animate-spin rounded-full h-12 w-12 border-4 border-sky-500 border-t-transparent mx-auto mb-4"></div>
              <div className="text-lg font-bold text-sky-700 mb-2">
                ✉️ Đang gửi mã xác minh
              </div>
              <div className="text-base font-medium text-gray-600">
                Mã sẽ được gửi đến email admin đã cấu hình
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            <div className="text-center bg-gradient-to-r from-emerald-50 to-teal-50 p-5 rounded-xl border-2 border-emerald-200 shadow-sm">
              <div className="text-lg font-bold text-emerald-700 mb-2">
                ✅ Email đã được gửi thành công!
              </div>
              <div className="text-base font-medium text-gray-600">
                Vui lòng kiểm tra hộp thư và nhập mã xác minh bên dưới
              </div>
            </div>
            
            <div className="space-y-4">
              <div className="space-y-3">
                <label className="block text-lg font-bold text-gray-700 text-center">
                  🔢 Nhập mã xác minh (6 chữ số)
                </label>
                <input
                  type="text"
                  value={code}
                  onChange={(e) => setCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                  placeholder="• • • • • •"
                  className="w-full px-6 py-4 border-3 border-sky-300 rounded-xl focus:ring-4 focus:ring-sky-200 focus:border-sky-500 text-center text-3xl font-bold text-gray-700 bg-gradient-to-r from-white to-sky-50 shadow-lg tracking-widest"
                  maxLength={6}
                  autoFocus
                />
              </div>

              {timeLeft > 0 && (
                <div className="text-center bg-gradient-to-r from-orange-50 to-amber-50 p-4 rounded-xl border-2 border-orange-200 shadow-sm">
                  <div className="text-base font-bold text-orange-700">
                    ⏰ Mã hết hạn sau: <span className="text-orange-800 text-lg">{formatTime(timeLeft)}</span>
                  </div>
                </div>
              )}

              <div className="flex gap-4 pt-6">
                <Button
                  variant="secondary"
                  onClick={handleClose}
                  className="flex-1 bg-gradient-to-r from-gray-100 to-gray-200 hover:from-gray-200 hover:to-gray-300 text-gray-700 font-bold border-2 border-gray-300 shadow-md hover:shadow-lg transition-all duration-200"
                >
                  ❌ Hủy
                </Button>
                <Button
                  variant="primary"
                  onClick={verifyCode}
                  loading={isLoading}
                  className="flex-1 bg-gradient-to-r from-sky-500 to-blue-500 hover:from-sky-600 hover:to-blue-600 text-white font-bold shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105 border-2 border-sky-400"
                  disabled={code.length !== 6}
                >
                  ✅ Xác minh
                </Button>
              </div>

              {timeLeft === 0 && (
                <div className="text-center pt-4">
                  <button
                    onClick={handleResendCode}
                    className="px-6 py-3 bg-gradient-to-r from-violet-500 to-purple-600 hover:from-violet-600 hover:to-purple-700 text-white font-bold rounded-lg shadow-md hover:shadow-lg transition-all duration-200 transform hover:scale-105"
                    disabled={isLoading}
                  >
                    🔄 Gửi lại mã xác minh
                  </button>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </Modal>
  )
}

export default AdminVerificationModal
