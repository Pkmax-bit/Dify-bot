'use client'

import { useState, useEffect, useMemo } from 'react'
import { format, parseISO } from 'date-fns'
import { vi } from 'date-fns/locale'
// Thêm icon RotateCw
import { Search, ServerCrash, Inbox, ChevronDown, BarChart2, CheckCircle, Clock, AlertTriangle, Cpu, Type, User, Bot, Calendar, RotateCw } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { motion, AnimatePresence } from 'framer-motion'
import DatePicker from 'react-datepicker'
import 'react-datepicker/dist/react-datepicker.css'
import './datepicker-custom.css'
import AdminLogoutButton from '@/app/components/admin/admin-logout-button'

// --- MAPPING & HELPERS ---
const ERROR_TYPE_COLORS = {
    'HTTPResponseCodeError': { bg: 'bg-red-100', text: 'text-red-800', hex: '#ef4444' },
    'n8n': { bg: 'bg-purple-100', text: 'text-purple-800', hex: '#a855f7' },
    'ValueError': { bg: 'bg-orange-100', text: 'text-orange-800', hex: '#f97316' },
    'TimeoutError': { bg: 'bg-yellow-100', text: 'text-yellow-800', hex: '#f59e0b' },
    'DatabaseError': { bg: 'bg-blue-100', text: 'text-blue-800', hex: '#3b82f6' },
    'Unknown': { bg: 'bg-slate-100', text: 'text-slate-800', hex: '#64748b' }
}

const getErrorColor = (type: string | null) => {
    if (!type) return ERROR_TYPE_COLORS['Unknown']
    
    if (type.includes('HTTPResponseCodeError')) return ERROR_TYPE_COLORS['HTTPResponseCodeError']
    if (type.toLowerCase() === 'n8n') return ERROR_TYPE_COLORS['n8n']
    if (type.includes('ValueError')) return ERROR_TYPE_COLORS['ValueError']
    if (type.includes('TimeoutError')) return ERROR_TYPE_COLORS['TimeoutError']
    if (type.includes('DatabaseError')) return ERROR_TYPE_COLORS['DatabaseError']
    
    return ERROR_TYPE_COLORS['Unknown']
}

const PIE_COLORS_ERROR_SOURCE = {
    'n8n': '#a855f7',
    'HTTP': '#ef4444',
    'Other': '#f97316'
}

interface ErrorLog {
    id: number
    error_message: string | null
    type_error: string | null
    node: string | null
    created_at: string
}

// --- MAIN COMPONENT ---
export default function AdminPage() {
    const [errors, setErrors] = useState<ErrorLog[]>([])
    const [status, setStatus] = useState('loading')
    const [searchTerm, setSearchTerm] = useState('')
    const [startDate, setStartDate] = useState<Date | null>(null)
    const [endDate, setEndDate] = useState<Date | null>(null)
    const [isRefreshing, setIsRefreshing] = useState(false) // State mới cho nút làm mới

    // Override global CSS to allow scrolling
    useEffect(() => {
        // Store original values
        const originalBodyOverflow = document.body.style.overflow
        const originalHtmlOverflow = document.documentElement.style.overflow
        
        // Enable scrolling
        document.body.style.overflow = 'auto'
        document.documentElement.style.overflow = 'auto'
        
        // Cleanup function to restore original values
        return () => {
            document.body.style.overflow = originalBodyOverflow || 'hidden'
            document.documentElement.style.overflow = originalHtmlOverflow || 'hidden'
        }
    }, [])

    const fetchErrors = async () => {
        try {
            const response = await fetch('/api/admin/supabase-error_logs?limit=100')
            if (response.ok) {
                const data = await response.json()
                if (data.success) {
                    setErrors(data.errors?.sort((a: ErrorLog, b: ErrorLog) => 
                        new Date(b.created_at).getTime() - new Date(a.created_at).getTime()) || [])
                    setStatus('success')
                }
            }
        } catch (err) {
            console.error('Error fetching error logs:', err)
            setStatus('error')
        }
    }

    // Hàm mới để xử lý việc nhấn nút làm mới
    const handleManualFetch = async () => {
        setIsRefreshing(true)
        await fetchErrors()
        // Thêm một chút delay để người dùng cảm nhận được việc làm mới
        setTimeout(() => setIsRefreshing(false), 500)
    }

    useEffect(() => {
        fetchErrors() // Fetch ban đầu

        // Auto refresh mỗi 30 giây
        const interval = setInterval(fetchErrors, 30000)
        return () => clearInterval(interval)
    }, [])

    const filteredErrors = useMemo(() => {
        if (!errors) return []
        return errors.filter(err => {
            // Text search filter
            const matchesSearch = (err.type_error || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
                (err.node || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
                (err.error_message || '').toLowerCase().includes(searchTerm.toLowerCase())
            
            // Date range filter
            const errorDate = new Date(err.created_at)
            const startDateTime = startDate ? new Date(startDate.getFullYear(), startDate.getMonth(), startDate.getDate()) : null
            const endDateTime = endDate ? new Date(endDate.getFullYear(), endDate.getMonth(), endDate.getDate(), 23, 59, 59) : null
            
            const matchesDateRange = (!startDateTime || errorDate >= startDateTime) &&
                                      (!endDateTime || errorDate <= endDateTime)
            
            return matchesSearch && matchesDateRange
        })
    }, [errors, searchTerm, startDate, endDate])

    if (status === 'loading') return <LoadingScreen />
    if (status === 'error') return <ErrorScreen />

    return (
        <div 
            className="w-full bg-slate-100" 
            style={{ 
                minHeight: '100vh', 
                overflow: 'auto',
                WebkitOverflowScrolling: 'touch' // For smooth scrolling on mobile
            }}
        >
            <div className="max-w-7xl mx-auto p-4 sm:p-8 pb-16">
                <header className="mb-8">
                    <div className="flex justify-between items-start">
                        <div>
                            <h1 className="text-4xl font-bold text-slate-900">Dashboard Giám Sát Lỗi</h1>
                            <p className="text-slate-500 mt-2">Phân tích và theo dõi các sự cố hệ thống từ Supabase.</p>
                        </div>
                        <div className="flex items-center gap-4">
                            <AdminLogoutButton />
                        </div>
                    </div>
                    
                    {/* Date Range Filter */}
                    <div className="mt-6 bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-xl shadow-lg border border-blue-200">
                        <h3 className="text-lg font-semibold text-blue-900 mb-4 flex items-center">
                            <Calendar className="w-5 h-5 mr-2 text-blue-600" />
                            Lọc theo thời gian
                        </h3>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
                            <div>
                                <label className="block text-sm font-medium text-blue-800 mb-2">
                                    Từ ngày
                                </label>
                                <div className="relative">
                                    <DatePicker
                                        selected={startDate}
                                        onChange={(date: Date | null) => setStartDate(date)}
                                        selectsStart
                                        startDate={startDate}
                                        endDate={endDate}
                                        placeholderText="Chọn ngày bắt đầu"
                                        dateFormat="dd/MM/yyyy"
                                        locale={vi}
                                        className="w-full px-4 py-3 border-2 border-blue-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-blue-900 font-medium shadow-sm cursor-pointer"
                                        wrapperClassName="w-full"
                                        showPopperArrow={false}
                                        popperClassName="react-datepicker-popper-custom"
                                    />
                                    <Calendar className="absolute right-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-blue-400 pointer-events-none" />
                                </div>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-blue-800 mb-2">
                                    Đến ngày
                                </label>
                                <div className="relative">
                                    <DatePicker
                                        selected={endDate}
                                        onChange={(date: Date | null) => setEndDate(date)}
                                        selectsEnd
                                        startDate={startDate}
                                        endDate={endDate}
                                        minDate={startDate ?? undefined}
                                        placeholderText="Chọn ngày kết thúc"
                                        dateFormat="dd/MM/yyyy"
                                        locale={vi}
                                        className="w-full px-4 py-3 border-2 border-blue-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-blue-900 font-medium shadow-sm cursor-pointer"
                                        wrapperClassName="w-full"
                                        showPopperArrow={false}
                                        popperClassName="react-datepicker-popper-custom"
                                    />
                                    <Calendar className="absolute right-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-blue-400 pointer-events-none" />
                                </div>
                            </div>
                            {/* Cập nhật khu vực các nút */}
                            <div className="flex flex-col sm:flex-row justify-center items-center gap-4">
                                <button
                                    onClick={() => {
                                        setStartDate(null)
                                        setEndDate(null)
                                    }}
                                    className="w-full sm:w-auto px-6 py-3 bg-gradient-to-r from-gray-500 to-gray-600 text-white rounded-lg hover:from-gray-600 hover:to-gray-700 transition-all duration-200 font-medium shadow-md transform hover:scale-105 flex items-center justify-center"
                                >
                                    🗑️ 
                                    <span className="ml-2">Xóa bộ lọc</span>
                                </button>
                                <button
                                    onClick={handleManualFetch}
                                    disabled={isRefreshing}
                                    className="w-full sm:w-auto px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all duration-200 font-medium shadow-md transform hover:scale-105 flex items-center justify-center disabled:opacity-75 disabled:cursor-not-allowed"
                                >
                                    <RotateCw className={`w-5 h-5 ${isRefreshing ? 'animate-spin' : ''}`} />
                                    <span className="ml-2">{isRefreshing ? 'Đang tải...' : 'Làm mới'}</span>
                                </button>
                            </div>
                        </div>
                        
                        {/* Display current filter status */}
                        {(startDate || endDate) && (
                            <div className="mt-4 p-4 bg-gradient-to-r from-emerald-50 to-teal-50 border-2 border-emerald-200 rounded-lg shadow-sm">
                                <p className="text-sm text-emerald-800 font-medium flex items-center">
                                    <CheckCircle className="w-4 h-4 mr-2 text-emerald-600" />
                                    <strong>Đang lọc:</strong>
                                    {startDate && ` Từ ${format(startDate, 'dd/MM/yyyy', { locale: vi })}`}
                                    {startDate && endDate && ' - '}
                                    {endDate && ` đến ${format(endDate, 'dd/MM/yyyy', { locale: vi })}`}
                                    {!startDate && endDate && ` Đến ${format(endDate, 'dd/MM/yyyy', { locale: vi })}`}
                                    {startDate && !endDate && ` từ ${format(startDate, 'dd/MM/yyyy', { locale: vi })} trở đi`}
                                </p>
                            </div>
                        )}
                    </div>
                </header>
                <ErrorAnalyticsSection 
                    errors={filteredErrors} 
                    totalErrors={errors.length}
                    isFiltered={filteredErrors.length !== errors.length}
                />
                <ErrorTable 
                    errors={filteredErrors} 
                    searchTerm={searchTerm} 
                    setSearchTerm={setSearchTerm}
                    totalErrors={errors.length}
                    filteredCount={filteredErrors.length}
                />
            </div>
        </div>
    )
}


// --- Các component con không thay đổi ---

// --- SHARED & SUB-COMPONENTS ---
const StatCard = ({ icon, title, value, unit, delay }: {
    icon: React.ReactNode
    title: string
    value: number
    unit: string
    delay: number
}) => (
    <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay }}
        className="bg-white p-6 rounded-xl shadow-md flex items-center space-x-4"
    >
        {icon}
        <div>
            <p className="text-sm text-slate-500 font-medium">{title}</p>
            <p className="text-2xl font-bold text-slate-800">
                {value}<span className="text-lg font-medium ml-1">{unit}</span>
            </p>
        </div>
    </motion.div>
)

const ErrorAnalyticsSection = ({ 
    errors, 
    totalErrors, 
    isFiltered 
}: { 
    errors: ErrorLog[]
    totalErrors: number
    isFiltered: boolean
}) => {
    const analytics = useMemo(() => {
        if (!errors || errors.length === 0) return { 
            total: 0, 
            uniqueNodes: 0, 
            uniqueErrorTypes: 0, 
            errorsByDay: [], 
            pieChartData: [] 
        }

        const errorsByDay = errors.reduce((acc: any[], err) => {
            const day = format(parseISO(err.created_at), 'yyyy-MM-dd')
            const entry = acc.find(d => d.name === day)
            if (entry) { 
                entry.errors++ 
            } else { 
                acc.push({ name: day, errors: 1 }) 
            }
            return acc
        }, []).sort((a, b) => new Date(a.name).getTime() - new Date(b.name).getTime())

        const errorSourceCounts = errors.reduce((acc: Record<string, number>, err) => {
            let source = 'Other'
            if (err.type_error?.toLowerCase() === 'n8n') source = 'n8n'
            else if (err.type_error?.includes('HTTPResponseCodeError')) source = 'HTTP'
            
            acc[source] = (acc[source] || 0) + 1
            return acc
        }, {})

        const uniqueOriginalErrorTypes = new Set(errors.map(err => err.type_error || 'Unknown')).size

        return {
            total: errors.length,
            uniqueNodes: new Set(errors.map(err => err.node)).size,
            uniqueErrorTypes: uniqueOriginalErrorTypes,
            errorsByDay,
            pieChartData: Object.entries(errorSourceCounts).map(([name, value]) => ({ name, value })),
        }
    }, [errors])

    return (
        <div className="mb-8">
            {isFiltered && (
                <div className="mb-4 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 border-2 border-blue-200 rounded-xl">
                    <p className="text-blue-800 font-medium text-center">
                        📊 <strong>Đang hiển thị kết quả đã lọc:</strong> {analytics.total} lỗi được chọn từ tổng {totalErrors} lỗi
                    </p>
                </div>
            )}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                <StatCard 
                    icon={<BarChart2 className="w-10 h-10 text-red-500" />} 
                    title={isFiltered ? "Số Lỗi (Đã lọc)" : "Tổng số Lỗi"} 
                    value={analytics.total} 
                    unit={isFiltered ? `/${totalErrors}` : ""} 
                    delay={0.1} 
                />
                <StatCard 
                    icon={<Cpu className="w-10 h-10 text-blue-500" />} 
                    title="Nền tảng bị lỗi" 
                    value={analytics.uniqueNodes} 
                    unit="" 
                    delay={0.2} 
                />
                <StatCard 
                    icon={<Type className="w-10 h-10 text-orange-500" />} 
                    title="Loại Lỗi Khác Nhau" 
                    value={analytics.uniqueErrorTypes} 
                    unit="" 
                    delay={0.3} 
                />
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
                <motion.div 
                    initial={{ opacity: 0, y: 20 }} 
                    animate={{ opacity: 1, y: 0 }} 
                    transition={{ duration: 0.5, delay: 0.4 }} 
                    className="lg:col-span-3 bg-white p-6 rounded-xl shadow-md"
                >
                    <h3 className="font-bold text-slate-800 mb-4">
                        {isFiltered ? "Số lượng lỗi theo ngày (Đã lọc)" : "Số lượng lỗi theo ngày"}
                    </h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={analytics.errorsByDay}>
                            <XAxis 
                                dataKey="name" 
                                stroke="#64748b" 
                                fontSize={12} 
                                tickLine={false} 
                                axisLine={false} 
                            />
                            <YAxis 
                                stroke="#64748b" 
                                fontSize={12} 
                                tickLine={false} 
                                axisLine={false} 
                            />
                            <Tooltip 
                                contentStyle={{ 
                                    backgroundColor: '#fff', 
                                    border: '1px solid #e2e8f0', 
                                    borderRadius: '0.5rem' 
                                }} 
                            />
                            <Bar 
                                dataKey="errors" 
                                fill="#ef4444" 
                                radius={[4, 4, 0, 0]} 
                            />
                        </BarChart>
                    </ResponsiveContainer>
                </motion.div>
                <motion.div 
                    initial={{ opacity: 0, y: 20 }} 
                    animate={{ opacity: 1, y: 0 }} 
                    transition={{ duration: 0.5, delay: 0.5 }} 
                    className="lg:col-span-2 bg-white p-6 rounded-xl shadow-md"
                >
                    <h3 className="font-bold text-slate-800 mb-4">
                        {isFiltered ? "Phân bố Nguồn Lỗi (Đã lọc)" : "Phân bố Nguồn Lỗi"}
                    </h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <PieChart>
                            <Pie 
                                data={analytics.pieChartData} 
                                dataKey="value" 
                                nameKey="name" 
                                cx="50%" 
                                cy="50%" 
                                outerRadius={100} 
                                label
                            >
                                {analytics.pieChartData.map((entry, index) => (
                                    <Cell 
                                        key={`cell-${index}`} 
                                        fill={PIE_COLORS_ERROR_SOURCE[entry.name as keyof typeof PIE_COLORS_ERROR_SOURCE] || '#64748b'} 
                                    />
                                ))}
                            </Pie>
                            <Tooltip 
                                contentStyle={{ 
                                    backgroundColor: '#fff', 
                                    border: '1px solid #e2e8f0', 
                                    borderRadius: '0.5rem' 
                                }} 
                            />
                            <Legend />
                        </PieChart>
                    </ResponsiveContainer>
                </motion.div>
            </div>
        </div>
    )
}

// Error Table
const ErrorTable = ({ errors, searchTerm, setSearchTerm, totalErrors, filteredCount }: {
    errors: ErrorLog[]
    searchTerm: string
    setSearchTerm: (term: string) => void
    totalErrors: number
    filteredCount: number
}) => (
    <div className="bg-white shadow-lg rounded-xl overflow-hidden">
        <div className="p-4 flex flex-col sm:flex-row justify-between items-start sm:items-center border-b border-slate-200 gap-4">
            <div>
                <h3 className="text-xl font-bold text-slate-800">Chi tiết Lỗi</h3>
                <p className="text-sm text-slate-600 mt-1">
                    Hiển thị {filteredCount} / {totalErrors} lỗi
                    {filteredCount !== totalErrors && (
                        <span className="text-blue-600 font-medium"> (đã lọc)</span>
                    )}
                </p>
            </div>
            <div className="relative">
                <span className="absolute inset-y-0 left-0 flex items-center pl-3">
                    <Search className="h-5 w-5 text-slate-400" />
                </span>
                <input 
                    type="text" 
                    placeholder="Tìm kiếm lỗi..." 
                    value={searchTerm} 
                    onChange={(e) => setSearchTerm(e.target.value)} 
                    className="w-full max-w-xs rounded-lg border border-slate-300 bg-white py-2 pl-10 pr-4 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500" 
                />
            </div>
        </div>
        <div className="overflow-y-auto" style={{ maxHeight: '500px' }}>
            <table className="min-w-full text-sm">
                <thead className="bg-slate-50 sticky top-0 z-10">
                    <tr className="text-left text-slate-600 uppercase tracking-wider font-medium">
                        <th className="p-4 w-12"></th>
                        <th className="p-4">Thời gian</th>
                        <th className="p-4">Node</th>
                        <th className="p-4">Loại Lỗi</th>
                        <th className="p-4">Thông báo</th>
                    </tr>
                </thead>
                <tbody>
                    {errors.length > 0 ? errors.map((err, index) => (
                        <ExpandableErrorRow key={err.id} error={err} index={index} />
                    )) : (
                        <NoDataFound message="Không có bản ghi lỗi nào khớp." />
                    )}
                </tbody>
            </table>
        </div>
    </div>
)

const ExpandableErrorRow = ({ error, index }: { error: ErrorLog; index: number }) => {
    const [isOpen, setIsOpen] = useState(false)
    const color = getErrorColor(error.type_error)
    
    return (
        <>
            <motion.tr 
                initial={{ opacity: 0 }} 
                animate={{ opacity: 1 }} 
                transition={{ duration: 0.3, delay: index * 0.05 }} 
                className="border-t border-slate-200 hover:bg-slate-50 cursor-pointer" 
                onClick={() => setIsOpen(!isOpen)}
            >
                <td className="p-4 text-center">
                    <motion.div animate={{ rotate: isOpen ? 180 : 0 }}>
                        <ChevronDown className="w-5 h-5 text-slate-400" />
                    </motion.div>
                </td>
                <td className="p-4 whitespace-nowrap text-slate-500">
                    {format(parseISO(error.created_at), 'dd/MM/yyyy HH:mm:ss', { locale: vi })}
                </td>
                <td className="p-4 font-mono text-blue-600">
                    {error.node || 'N/A'}
                </td>
                <td className="p-4">
                    <span className={`px-2.5 py-1 rounded-full text-xs font-semibold leading-tight ${color.bg} ${color.text}`}>
                        {error.type_error?.includes('HTTPResponseCodeError') ? 'HTTP Error' :
                         error.type_error?.toLowerCase() === 'n8n' ? 'n8n' :
                         error.type_error || 'Unknown'}
                    </span>
                </td>
                <td className="p-4 max-w-md truncate text-slate-800">
                    {error.error_message || 'Không có thông báo'}
                </td>
            </motion.tr>
            <AnimatePresence>
                {isOpen && (
                    <motion.tr 
                        initial={{ opacity: 0, height: 0 }} 
                        animate={{ opacity: 1, height: 'auto' }} 
                        exit={{ opacity: 0, height: 0 }} 
                        transition={{ duration: 0.3, ease: "easeInOut" }}
                    >
                        <td colSpan={5} className="p-0">
                            <div className="bg-slate-50 p-6">
                                <h4 className="font-bold text-slate-700 mb-2">Chi tiết thông báo lỗi:</h4>
                                <div className="bg-white p-4 rounded-md border border-slate-200">
                                    <div className="space-y-3">
                                        <div>
                                            <span className="font-semibold text-slate-600">Error ID:</span>
                                            <span className="ml-2 font-mono text-blue-600">#{error.id}</span>
                                        </div>
                                        {error.type_error && (
                                            <div>
                                                <span className="font-semibold text-slate-600">Type Error:</span>
                                                <span className="ml-2 font-mono text-slate-800">{error.type_error}</span>
                                            </div>
                                        )}
                                        {error.error_message && (
                                            <div>
                                                <span className="font-semibold text-slate-600">Message:</span>
                                                <pre className="mt-2 p-3 bg-red-50 border border-red-200 rounded text-sm text-red-700 whitespace-pre-wrap font-mono">
                                                    {error.error_message}
                                                </pre>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>
                        </td>
                    </motion.tr>
                )}
            </AnimatePresence>
        </>
    )
}

// Helper Screens
const LoadingScreen = () => (
    <div className="flex h-screen items-center justify-center bg-slate-100">
        <div className="w-16 h-16 border-4 border-dashed rounded-full animate-spin border-blue-500"></div>
    </div>
)

const ErrorScreen = () => (
    <div className="flex h-screen items-center justify-center bg-slate-100 text-center">
        <div>
            <ServerCrash className="w-16 h-16 text-red-500 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-slate-800">Lỗi kết nối</h2>
            <p className="text-slate-500">Không thể tải dữ liệu. Vui lòng thử lại sau.</p>
        </div>
    </div>
)

const NoDataFound = ({ message }: { message: string }) => (
    <tr>
        <td colSpan={5} className="text-center py-16">
            <Inbox className="w-16 h-16 text-slate-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-slate-700">Không tìm thấy dữ liệu</h3>
            <p className="text-slate-500">{message}</p>
        </td>
    </tr>
)