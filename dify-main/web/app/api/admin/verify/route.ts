import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const adminKey = request.headers.get('X-Admin-Key')
    
    if (!adminKey) {
      return NextResponse.json({ error: 'Admin Key required' }, { status: 401 })
    }

    // Forward to Flask API for verification
    const response = await fetch(`${process.env.CONSOLE_API_URL || 'http://localhost:5001'}/console/api/admin/verify`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Admin-Key': adminKey
      }
    })

    if (response.ok) {
      return NextResponse.json({ success: true })
    } else {
      return NextResponse.json({ error: 'Invalid admin key' }, { status: 401 })
    }
  } catch (error) {
    console.error('Error verifying admin key:', error)
    return NextResponse.json({ error: 'Server error' }, { status: 500 })
  }
}
