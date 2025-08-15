'use client'

import React, { useState, useEffect } from 'react'
import { 
  RiRobot2Line, 
  RiSparklingLine,
  RiChatSmile2Line, 
  RiBarChartLine,
  RiAppsLine,
  RiArrowLeftLine
} from '@remixicon/react'
import Button from '@/app/components/base/button'
import { fetchAppList } from '@/service/apps'
import type { App } from '@/types/app'
import Loading from '@/app/components/base/loading'
import Toast from '@/app/components/base/toast'
import styles from './styles.module.css'

// Import the published app chat components
import EmbeddedChatbot from '@/app/components/base/chat/embedded-chatbot'

type FilterStatus = 'all' | 'published' | 'draft'

// Quick Chat Embedded Wrapper Component  
const QuickChatEmbeddedWrapper = ({ app }: { app: App }) => {
  const [embedUrl, setEmbedUrl] = useState<string>('')
  const [isActivating, setIsActivating] = useState<boolean>(false)
  const [activatedApp, setActivatedApp] = useState<App>(app)

  const activateSiteIfNeeded = async () => {
    if (activatedApp.site?.access_token) return // Already has site enabled
    
    setIsActivating(true)
    try {
      // Auto-enable site for the app using correct endpoint
      const response = await fetch(`/console/api/apps/${activatedApp.id}/site`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          enable_site: true,
          title: activatedApp.name,
          author: 'Quick Chat V2',
          description: `Chat interface for ${activatedApp.name}`,
          default_language: 'vi-VN',
          prompt_public: false,
          copyright: '',
          privacy_policy: '',
          custom_disclaimer: ''
        })
      })
      
      if (response.ok) {
        const data = await response.json()
        const updatedApp = {
          ...activatedApp,
          enable_site: true,
          site: data
        }
        setActivatedApp(updatedApp)
      }
    } catch (error) {
      console.error('Failed to enable site:', error)
    } finally {
      setIsActivating(false)
    }
  }

  useEffect(() => {
    // If app has site enabled and access token, use the shared URL
    if (activatedApp.site?.access_token) {
      // Construct the embed URL for this app
      const baseUrl = window.location.origin
      const sharedUrl = `${baseUrl}/share/${activatedApp.site.access_token}`
      setEmbedUrl(sharedUrl)
    } else {
      // Try to auto-activate
      activateSiteIfNeeded()
    }
  }, [activatedApp])

  // If activating, show loading
  if (isActivating) {
    return (
      <div className="flex-1 h-full flex items-center justify-center">
        <div className="text-center max-w-md px-8">
          <div className="w-24 h-24 bg-gradient-to-br from-blue-500 to-purple-600 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-lg animate-pulse">
            <span className="text-3xl">⚡</span>
          </div>
          <h3 className="text-xl font-bold mb-4 text-gray-900">
            Đang kích hoạt chat...
          </h3>
          <p className="text-gray-600">
            Đang thiết lập chat trực tiếp cho "{activatedApp.name}"
          </p>
        </div>
      </div>
    )
  }

  // If no embed URL available, show a setup message
  if (!embedUrl) {
    return (
      <div className="flex-1 h-full flex items-center justify-center">
        <div className="text-center max-w-md px-8">
          <div className="w-24 h-24 bg-gradient-to-br from-red-500 to-orange-500 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-lg">
            <span className="text-3xl">🔧</span>
          </div>
          <h3 className="text-xl font-bold mb-4 text-gray-900">
            Không thể kích hoạt chat
          </h3>
          <p className="text-gray-600 mb-6">
            Không thể tự động kích hoạt tính năng Site cho ứng dụng "{activatedApp.name}". 
            Vui lòng kích hoạt thủ công trong cài đặt ứng dụng.
          </p>
          <button
            onClick={activateSiteIfNeeded}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
          >
            Thử lại
          </button>
        </div>
      </div>
    )
  }

  // Render iframe with the shared app
  return (
    <div className="flex-1 h-full">
      <iframe
        src={embedUrl}
        className="w-full h-full border-0 rounded-lg"
        title={`Chat với ${activatedApp.name}`}
        allow="microphone; camera; clipboard-write"
        sandbox="allow-scripts allow-same-origin allow-forms allow-popups allow-popups-to-escape-sandbox"
      />
    </div>
  )
}

export default function QuickChatV2() {
  const [apps, setApps] = useState<App[]>([])
  const [selectedApp, setSelectedApp] = useState<App | null>(null)
  const [appsLoading, setAppsLoading] = useState(true)
  const [showAppList, setShowAppList] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [filterStatus, setFilterStatus] = useState<FilterStatus>('all')
  const [darkMode, setDarkMode] = useState(false)

  // Load apps on component mount
  useEffect(() => {
    loadApps()
  }, [])

  // Load dark mode preference
  useEffect(() => {
    const savedDarkMode = localStorage.getItem('quickChatV2DarkMode')
    if (savedDarkMode) {
      setDarkMode(JSON.parse(savedDarkMode))
    }
  }, [])

  // Save dark mode preference
  useEffect(() => {
    localStorage.setItem('quickChatV2DarkMode', JSON.stringify(darkMode))
  }, [darkMode])

  const loadApps = async () => {
    try {
      setAppsLoading(true)
      const response = await fetchAppList({ url: '/apps', params: { page: 1 } })
      if (response && response.data) {
        setApps(response.data)
        
        // Auto-select first app if available
        if (response.data.length > 0 && !selectedApp) {
          setSelectedApp(response.data[0])
        }
      }
    } catch (error) {
      console.error('Error loading apps:', error)
      Toast.notify({
        type: 'error',
        message: 'Không thể tải danh sách ứng dụng. Vui lòng thử lại.'
      })
    } finally {
      setAppsLoading(false)
      setShowAppList(false)
    }
  }

  const filteredApps = apps.filter(app => {
    const matchesSearch = app.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         app.description?.toLowerCase().includes(searchQuery.toLowerCase())
    
    const matchesFilter = filterStatus === 'all' || 
                         (filterStatus === 'published' && (app.enable_api || app.enable_site)) ||
                         (filterStatus === 'draft' && !app.enable_api && !app.enable_site)
    
    return matchesSearch && matchesFilter
  })

  const getAppTypeIcon = (mode: string) => {
    switch (mode) {
      case 'chat': return RiChatSmile2Line
      case 'workflow': return RiBarChartLine
      case 'agent': return RiRobot2Line
      default: return RiSparklingLine
    }
  }

  const selectApp = (app: App) => {
    setSelectedApp(app)
    setShowAppList(false)
  }

  if (appsLoading) {
    return (
      <div className={`min-h-screen flex items-center justify-center transition-all duration-300 ${
        darkMode 
          ? 'bg-gradient-to-br from-slate-900 via-gray-900 to-slate-800' 
          : 'bg-gradient-to-br from-blue-50 via-white to-purple-50'
      }`}>
        <div className="flex flex-col items-center space-y-4">
          <div className="relative">
            <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-3xl flex items-center justify-center shadow-2xl">
              <RiSparklingLine className="w-8 h-8 text-white animate-pulse" />
            </div>
          </div>
          <div className="text-center">
            <h3 className={`text-xl font-bold mb-2 transition-colors duration-300 ${
              darkMode ? 'text-white' : 'text-gray-900'
            }`}>
              ⚡ Đang tải Dify Quick Chat V2...
            </h3>
            <Loading type='area' />
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className={`${styles.container} ${
      darkMode ? styles.containerDark : styles.containerLight
    }`}>
      {/* Enhanced Header */}
      <div className={`${styles.header} ${
        darkMode ? styles.headerDark : styles.headerLight
      }`}>
        <div className={styles.headerContent}>
          <div className={styles.headerLeft}>
            <div className={styles.headerIcon}>
              <div className={styles.headerIconGradient}>
                <RiSparklingLine className="w-6 h-6 text-white" />
              </div>
              <div className={styles.headerIconBadge}></div>
            </div>
            <div>
              <h1 className={`${styles.headerTitle} ${
                darkMode ? styles.headerTitleDark : styles.headerTitleLight
              }`}>
                ⚡ Dify Quick Chat V2
              </h1>
              <p className={`${styles.headerSubtitle} ${
                darkMode ? styles.headerSubtitleDark : styles.headerSubtitleLight
              }`}>
                {selectedApp ? (
                  <span className="flex items-center space-x-2">
                    <span>Đang trò chuyện với</span>
                    <span className={`px-2 py-1 rounded-lg text-xs font-semibold ${
                      darkMode 
                        ? 'bg-blue-900/50 text-blue-200' 
                        : 'bg-blue-100 text-blue-800'
                    }`}>
                      {selectedApp.name}
                    </span>
                  </span>
                ) : (
                  'Giao diện chat mới - Thân thiện và dễ sử dụng'
                )}
              </p>
            </div>
          </div>
          
          <div className={styles.headerActions}>
            {/* App List Toggle */}
            <Button
              variant="secondary"
              size="small"
              onClick={() => setShowAppList(!showAppList)}
              className={`${styles.appListButton} ${
                showAppList 
                  ? darkMode ? styles.appListButtonActiveDark : styles.appListButtonActiveLight
                  : darkMode ? styles.appListButtonInactiveDark : styles.appListButtonInactiveLight
              }`}
            >
              <RiAppsLine className="w-4 h-4" />
              <span className="font-medium">Ứng dụng ({apps.length})</span>
            </Button>

            <Button
              variant="secondary"
              size="small"
              onClick={() => window.location.href = '/apps'}
              className={`${styles.workspaceButton} ${
                darkMode ? styles.workspaceButtonDark : styles.workspaceButtonLight
              }`}
            >
              <RiArrowLeftLine className="w-4 h-4" />
              <RiAppsLine className="w-4 h-4" />
              <span>🏠 Về Workspace</span>
            </Button>
          </div>
        </div>
      </div>

      <div className="flex-1 flex overflow-hidden">
        {/* App Selector Sidebar */}
        {showAppList && (
          <div className={`w-96 border-r flex flex-col shadow-xl transition-all duration-300 ${
            darkMode
              ? 'bg-slate-900 border-slate-600'
              : 'bg-white border-slate-400'
          }`}>
            <div className={`p-6 border-b transition-colors duration-300 ${
              darkMode ? 'border-slate-600' : 'border-slate-300'
            }`}>
              <div className="flex items-center justify-between mb-4">
                <h3 className={`font-bold text-xl transition-colors duration-300 ${
                  darkMode ? 'text-white' : 'text-gray-900'
                }`}>
                  📱 Ứng dụng có sẵn
                </h3>
              </div>
              
              {/* Search */}
              <div className="space-y-3">
                <div className="relative">
                  <input
                    type="text"
                    placeholder="🔍 Tìm kiếm ứng dụng..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className={`w-full px-4 py-3 pl-10 rounded-xl border-2 focus:outline-none focus:ring-2 transition-all duration-300 font-medium ${
                      darkMode
                        ? 'bg-slate-800 border-slate-500 text-white placeholder-slate-400 focus:ring-blue-500 focus:border-blue-500'
                        : 'bg-white border-slate-400 text-slate-900 placeholder-slate-600 focus:ring-blue-500 focus:border-blue-500'
                    }`}
                  />
                </div>
                
                <div className="flex space-x-2">
                  {['all', 'published', 'draft'].map((filter) => (
                    <button
                      key={filter}
                      onClick={() => setFilterStatus(filter as any)}
                      className={`px-4 py-2 text-sm rounded-xl font-semibold transition-all duration-300 ${
                        filterStatus === filter
                          ? 'bg-blue-600 text-white shadow-lg'
                          : darkMode
                            ? 'bg-slate-800 text-white border-2 border-slate-600'
                            : 'bg-slate-100 text-slate-900 border-2 border-slate-400'
                      }`}
                    >
                      {filter === 'all' ? '📋 Tất cả' : filter === 'published' ? '🌐 Đã xuất bản' : '📝 Bản nháp'}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Apps List */}
            <div className="flex-1 overflow-y-auto">
              <div className="p-4 space-y-2">
                {filteredApps.map((app) => (
                  <div
                    key={app.id}
                    onClick={() => selectApp(app)}
                    className={`group relative p-4 rounded-2xl border-2 cursor-pointer transition-all duration-300 hover:shadow-lg ${
                      selectedApp?.id === app.id
                        ? darkMode
                          ? 'bg-blue-900/30 border-blue-400 shadow-lg shadow-blue-500/20'
                          : 'bg-blue-50 border-blue-400 shadow-lg shadow-blue-500/20'
                        : darkMode
                          ? 'bg-slate-800 border-slate-600 hover:border-slate-400 hover:bg-slate-700'
                          : 'bg-white border-slate-300 hover:border-slate-400 hover:bg-slate-50'
                    }`}
                  >
                    {/* App Icon and Basic Info */}
                    <div className="flex items-center space-x-4 mb-3">
                      <div className="relative">
                        <div className="w-12 h-12 bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 rounded-2xl flex items-center justify-center shadow-lg">
                          {React.createElement(getAppTypeIcon(app.mode), { className: "w-6 h-6 text-white" })}
                        </div>
                        {(app.enable_api || app.enable_site) && (
                          <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-400 rounded-full border-2 border-white"></div>
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <h4 className={`font-bold text-lg truncate transition-colors duration-300 ${
                          darkMode ? 'text-white' : 'text-gray-900'
                        }`}>
                          {app.name}
                        </h4>
                        <div className="flex items-center space-x-2 mt-1">
                          <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded-lg text-xs font-semibold capitalize">
                            {app.mode}
                          </span>
                        </div>
                      </div>
                    </div>

                    {/* Status Info */}
                    <div className="space-y-3">
                      <div className="grid grid-cols-2 gap-2 text-xs">
                        <div className={`p-2 rounded-lg text-center transition-colors duration-300 ${
                          app.enable_api 
                            ? darkMode ? 'bg-green-900/30 text-green-300' : 'bg-green-50 text-green-700'
                            : darkMode ? 'bg-red-900/30 text-red-300' : 'bg-red-50 text-red-700'
                        }`}>
                          API: {app.enable_api ? 'BẬT' : 'TẮT'}
                        </div>
                        <div className={`p-2 rounded-lg text-center transition-colors duration-300 ${
                          app.enable_site 
                            ? darkMode ? 'bg-green-900/30 text-green-300' : 'bg-green-50 text-green-700'
                            : darkMode ? 'bg-red-900/30 text-red-300' : 'bg-red-50 text-red-700'
                        }`}>
                          Web: {app.enable_site ? 'BẬT' : 'TẮT'}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}

                {filteredApps.length === 0 && (
                  <div className={`text-center py-12 transition-colors duration-300 ${
                    darkMode ? 'text-slate-400' : 'text-slate-500'
                  }`}>
                    <p className="text-sm">Không tìm thấy ứng dụng nào</p>
                    <p className="text-xs mt-1">Thử thay đổi từ khóa tìm kiếm hoặc bộ lọc</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Chat Area - Using Published App's Chat Component */}
        <div className="flex-1 flex flex-col">
          {selectedApp ? (
            <div className="flex-1 flex flex-col">
              {/* Simple Header */}
              <div className={`border-b px-6 py-4 flex items-center justify-between shadow-sm transition-all duration-300 ${
                darkMode 
                  ? 'bg-slate-900 border-slate-600' 
                  : 'bg-white border-slate-300'
              }`}>
                <div className="flex items-center space-x-4">
                  <div className="relative">
                    <div className="w-12 h-12 bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 rounded-2xl flex items-center justify-center shadow-lg">
                      {React.createElement(getAppTypeIcon(selectedApp.mode), { className: "w-6 h-6 text-white" })}
                    </div>
                    <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-green-400 rounded-full border-2 border-white animate-pulse"></div>
                  </div>
                  <div>
                    <h3 className={`font-bold text-lg ${darkMode ? 'text-white' : 'text-gray-900'}`}>{selectedApp.name}</h3>
                    <div className="flex items-center space-x-3 mt-1">
                      <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded-lg text-xs font-semibold capitalize">
                        {selectedApp.mode}
                      </span>
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center space-x-3">
                  <Button
                    variant="ghost"
                    size="small"
                    onClick={() => setShowAppList(true)}
                    className="text-blue-600 hover:text-blue-800"
                  >
                    <RiAppsLine className="w-4 h-4 mr-1" />
                    Chuyển ứng dụng
                  </Button>
                </div>
              </div>

              {/* Embedded Chat Component */}
              <div className="flex-1 h-full">
                <QuickChatEmbeddedWrapper app={selectedApp} />
              </div>
            </div>
          ) : (
            /* No App Selected */
            <div className={`flex-1 flex items-center justify-center transition-all duration-300 ${
              darkMode
                ? 'bg-gradient-to-br from-gray-800/50 to-slate-900/50'
                : 'bg-gradient-to-br from-blue-50/50 to-purple-50/50'
            }`}>
              <div className="text-center max-w-lg px-8">
                <div className="relative mb-8">
                  <div className={`w-32 h-32 rounded-3xl flex items-center justify-center mx-auto shadow-2xl transition-all duration-300 ${
                    darkMode
                      ? 'bg-gradient-to-br from-blue-600 via-purple-700 to-pink-700'
                      : 'bg-gradient-to-br from-blue-400 via-purple-500 to-pink-500'
                  }`}>
                    <RiSparklingLine className="w-16 h-16 text-white animate-pulse" />
                  </div>
                  <div className={`absolute -top-3 -right-3 w-12 h-12 rounded-2xl flex items-center justify-center shadow-lg animate-bounce ${
                    darkMode
                      ? 'bg-yellow-500'
                      : 'bg-yellow-400'
                  }`}>
                    <RiChatSmile2Line className={`w-6 h-6 ${
                      darkMode ? 'text-yellow-900' : 'text-yellow-800'
                    }`} />
                  </div>
                </div>
                
                <h2 className={`text-4xl font-bold mb-6 transition-colors duration-300 ${
                  darkMode
                    ? 'bg-gradient-to-r from-white via-blue-200 to-purple-200 bg-clip-text text-transparent'
                    : 'bg-gradient-to-r from-gray-900 via-blue-800 to-purple-800 bg-clip-text text-transparent'
                }`}>
                  ⚡ Dify Quick Chat V2
                </h2>
                
                <p className={`mb-8 leading-relaxed text-lg transition-colors duration-300 ${
                  darkMode ? 'text-gray-300' : 'text-gray-600'
                }`}>
                  🚀 Chào mừng bạn đến với Quick Chat V2! 
                  <br />
                  ✨ Giao diện mới - Thân thiện - Dễ sử dụng
                </p>
                
                <Button
                  variant="primary"
                  onClick={() => setShowAppList(true)}
                  className={`px-8 py-4 text-lg font-bold rounded-2xl shadow-2xl transition-all duration-300 transform hover:scale-105 ${
                    darkMode
                      ? 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700'
                      : 'bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700'
                  }`}
                >
                  <RiAppsLine className="w-6 h-6 mr-3" />
                  🎯 Chọn Ứng Dụng Để Bắt Đầu
                </Button>
                
                <div className="mt-8 grid grid-cols-3 gap-4 text-sm">
                  <div className={`p-4 rounded-2xl transition-all duration-300 ${
                    darkMode
                      ? 'bg-slate-800/50 border border-slate-600'
                      : 'bg-white/50 border border-slate-200'
                  }`}>
                    <RiChatSmile2Line className={`w-8 h-8 mx-auto mb-2 ${
                      darkMode ? 'text-blue-400' : 'text-blue-500'
                    }`} />
                    <p className={`font-semibold transition-colors duration-300 ${
                      darkMode ? 'text-white' : 'text-gray-900'
                    }`}>
                      Chat Thông Minh
                    </p>
                    <p className={`text-xs mt-1 transition-colors duration-300 ${
                      darkMode ? 'text-gray-400' : 'text-gray-500'
                    }`}>
                      Trò chuyện với AI
                    </p>
                  </div>
                  
                  <div className={`p-4 rounded-2xl transition-all duration-300 ${
                    darkMode
                      ? 'bg-slate-800/50 border border-slate-600'
                      : 'bg-white/50 border border-slate-200'
                  }`}>
                    <RiBarChartLine className={`w-8 h-8 mx-auto mb-2 ${
                      darkMode ? 'text-purple-400' : 'text-purple-500'
                    }`} />
                    <p className={`font-semibold transition-colors duration-300 ${
                      darkMode ? 'text-white' : 'text-gray-900'
                    }`}>
                      Workflow
                    </p>
                    <p className={`text-xs mt-1 transition-colors duration-300 ${
                      darkMode ? 'text-gray-400' : 'text-gray-500'
                    }`}>
                      Tự động hóa
                    </p>
                  </div>
                  
                  <div className={`p-4 rounded-2xl transition-all duration-300 ${
                    darkMode
                      ? 'bg-slate-800/50 border border-slate-600'
                      : 'bg-white/50 border border-slate-200'
                  }`}>
                    <RiRobot2Line className={`w-8 h-8 mx-auto mb-2 ${
                      darkMode ? 'text-pink-400' : 'text-pink-500'
                    }`} />
                    <p className={`font-semibold transition-colors duration-300 ${
                      darkMode ? 'text-white' : 'text-gray-900'
                    }`}>
                      Agent
                    </p>
                    <p className={`text-xs mt-1 transition-colors duration-300 ${
                      darkMode ? 'text-gray-400' : 'text-gray-500'
                    }`}>
                      Trợ lý AI
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
