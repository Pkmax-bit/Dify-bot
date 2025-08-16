import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  try {
    // Forward to Flask API
    const response = await fetch(`${process.env.CONSOLE_API_URL || 'http://localhost:5001'}/console/api/admin/error-sync/status`, {
      headers: {
        'Content-Type': 'application/json'
      }
    })

    if (response.ok) {
      const data = await response.json()
      // Extract the nested status object if it exists
      if (data.success && data.status) {
        return NextResponse.json(data.status)
      }
      return NextResponse.json(data)
    } else {
      return NextResponse.json({ error: 'Failed to fetch error sync status' }, { status: response.status })
    }
  } catch (error) {
    console.error('Error fetching error sync status:', error)
    return NextResponse.json({ error: 'Server error' }, { status: 500 })
  }
}
