import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    // Forward to Flask API
    const response = await fetch(`${process.env.CONSOLE_API_URL || 'http://localhost:5001'}/console/api/admin/error-sync/stop`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })

    if (response.ok) {
      const data = await response.json()
      return NextResponse.json(data)
    } else {
      return NextResponse.json({ error: 'Failed to stop error sync' }, { status: response.status })
    }
  } catch (error) {
    console.error('Error stopping error sync:', error)
    return NextResponse.json({ error: 'Server error' }, { status: 500 })
  }
}
