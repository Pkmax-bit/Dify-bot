import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  try {
    const adminKey = request.headers.get('X-Admin-Key')
    
    if (!adminKey) {
      return NextResponse.json({ error: 'Admin Key required' }, { status: 401 })
    }

    // Forward to Flask API
    const response = await fetch(`${process.env.CONSOLE_API_URL || 'http://localhost:5001'}/console/api/admin/logs/errors`, {
      headers: {
        'X-Admin-Key': adminKey
      }
    })

    if (response.ok) {
      const data = await response.json()
      return NextResponse.json(data)
    } else {
      return NextResponse.json({ error: 'Failed to fetch error logs' }, { status: response.status })
    }
  } catch (error) {
    console.error('Error fetching error logs:', error)
    return NextResponse.json({ error: 'Server error' }, { status: 500 })
  }
}
