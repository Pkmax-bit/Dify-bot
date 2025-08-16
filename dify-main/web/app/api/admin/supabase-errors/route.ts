import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  try {
    // Get query parameters from the request
    const { searchParams } = new URL(request.url)
    const limit = searchParams.get('limit') || '50'
    
    const response = await fetch(`http://localhost:5001/console/api/admin/supabase-errors?limit=${limit}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      const errorText = await response.text()
      console.error('Backend error:', errorText)
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error fetching Supabase errors:', error)
    return NextResponse.json(
      { success: false, error: 'Failed to fetch Supabase errors' },
      { status: 500 }
    )
  }
}
