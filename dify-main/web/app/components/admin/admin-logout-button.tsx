'use client'

import React, { useState } from 'react'
import { useRouter } from 'next/navigation'
import { RiLogoutBoxRLine, RiShieldCheckLine } from '@remixicon/react'
import Button from '@/app/components/base/button'
import Modal from '@/app/components/base/modal'
import Toast from '@/app/components/base/toast'

const AdminLogoutButton = () => {
  const router = useRouter()
  const [showConfirm, setShowConfirm] = useState(false)
  const [isLoggingOut, setIsLoggingOut] = useState(false)

  const handleLogout = async () => {
    setIsLoggingOut(true)
    try {
      // Get session info from localStorage
      const sessionId = localStorage.getItem('admin_session_id')
      
      // Call logout API
      if (sessionId) {
        await fetch('/console/api/admin/logout', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'x-session-id': sessionId,
          },
          body: JSON.stringify({ session_id: sessionId }),
        })
      }

      // Clear all admin session data
      localStorage.removeItem('admin_session_token')
      localStorage.removeItem('admin_session_expires')
      localStorage.removeItem('admin_session_id')

      // Clear cookies
      document.cookie = 'admin_session_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'
      document.cookie = 'admin_session_expires=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'
      document.cookie = 'admin_session_id=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'

      Toast.notify({ type: 'success', message: 'Đã đăng xuất khỏi Admin Dashboard an toàn' })
      
      // Close modal and redirect
      setShowConfirm(false)
      router.push('/')
      
    } catch (error) {
      console.error('Logout error:', error)
      Toast.notify({ type: 'error', message: 'Lỗi khi đăng xuất' })
    } finally {
      setIsLoggingOut(false)
    }
  }

  return (
    <>
      <Button
        variant="secondary"
        size="medium"
        onClick={() => setShowConfirm(true)}
        className="flex items-center gap-2 bg-gradient-to-r from-orange-50 to-red-50 hover:from-orange-100 hover:to-red-100 text-orange-600 border-2 border-orange-200 hover:border-orange-300 font-semibold shadow-md hover:shadow-lg transition-all duration-200 transform hover:scale-105"
      >
        <RiLogoutBoxRLine className="w-4 h-4" />
        Thoát Admin
      </Button>

      <Modal
        isShow={showConfirm}
        onClose={() => setShowConfirm(false)}
        className="!max-w-md"
      >
        <div className="p-8 bg-gradient-to-br from-sky-50 via-white to-emerald-50 border-2 border-sky-200 rounded-2xl">
          <div className="flex items-center gap-4 mb-6">
            <div className="flex items-center justify-center w-16 h-16 bg-gradient-to-br from-sky-100 to-emerald-100 rounded-2xl shadow-lg border-2 border-sky-300">
              <RiShieldCheckLine className="w-8 h-8 text-sky-600" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-gray-700 mb-1">
                Xác nhận thoát Admin
              </h3>
              <p className="text-base text-gray-600 font-medium">
                Bạn có chắc chắn muốn thoát khỏi Admin Dashboard?
              </p>
            </div>
          </div>

          <div className="space-y-4 mb-8">
            <div className="text-base text-gray-700 font-medium bg-gradient-to-r from-sky-50 to-blue-50 p-4 rounded-xl border-2 border-sky-200 shadow-sm">
              🔒 Khi thoát, session admin của bạn sẽ được xóa hoàn toàn để đảm bảo bảo mật:
            </div>
            <ul className="text-base text-gray-600 space-y-3 bg-gradient-to-r from-emerald-50 to-teal-50 p-5 rounded-xl border-2 border-emerald-200 shadow-sm">
              <li className="flex items-center gap-3">
                <span className="w-3 h-3 bg-gradient-to-r from-sky-400 to-blue-500 rounded-full shadow-sm"></span>
                <span className="font-medium">Xóa session token khỏi server</span>
              </li>
              <li className="flex items-center gap-3">
                <span className="w-3 h-3 bg-gradient-to-r from-emerald-400 to-teal-500 rounded-full shadow-sm"></span>
                <span className="font-medium">Xóa dữ liệu session khỏi trình duyệt</span>
              </li>
              <li className="flex items-center gap-3">
                <span className="w-3 h-3 bg-gradient-to-r from-violet-400 to-purple-500 rounded-full shadow-sm"></span>
                <span className="font-medium">Chuyển hướng về trang chủ an toàn</span>
              </li>
            </ul>
          </div>

          <div className="flex gap-4">
            <Button
              variant="secondary"
              onClick={() => setShowConfirm(false)}
              className="flex-1 bg-gradient-to-r from-slate-100 to-gray-100 hover:from-slate-200 hover:to-gray-200 text-gray-600 font-bold border-2 border-slate-300 hover:border-slate-400 shadow-md hover:shadow-lg transition-all duration-200 transform hover:scale-105"
              disabled={isLoggingOut}
            >
              ❌ Hủy
            </Button>
            <Button
              variant="primary"
              onClick={handleLogout}
              loading={isLoggingOut}
              className="flex-1 bg-gradient-to-r from-sky-500 to-blue-500 hover:from-sky-600 hover:to-blue-600 text-white font-bold shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105 border-2 border-sky-400"
            >
              ✅ Thoát an toàn
            </Button>
          </div>
        </div>
      </Modal>
    </>
  )
}

export default AdminLogoutButton
