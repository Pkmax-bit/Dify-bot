import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  try {
    // Call the backend endpoint for Dify logs
    const response = await fetch('http://localhost:5001/api/admin/logs', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      throw new Error(`Backend responded with status: ${response.status}`)
    }

    const data = await response.json()
    
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error fetching Dify logs:', error)
    
    // Return mock data for development
    const mockLogs = [
      {
        id: 1,
        workflow_run_id: 'wf_12345678-1234-5678-9abc-123456789012',
        conversation_id: 'conv_87654321-4321-8765-dcba-987654321098',
        input_text: 'What is machine learning?',
        output_text: 'Machine learning is a subset of artificial intelligence...',
        status: 'completed',
        created_at: new Date(Date.now() - 1000 * 60 * 5).toISOString(), // 5 minutes ago
        latency_ms: 1250,
        user_id: 'user_001'
      },
      {
        id: 2,
        workflow_run_id: 'wf_23456789-2345-6789-abcd-234567890123',
        conversation_id: 'conv_76543210-3210-7654-cba9-876543210987',
        input_text: 'Generate a Python script for data analysis',
        output_text: null,
        status: 'failed',
        created_at: new Date(Date.now() - 1000 * 60 * 10).toISOString(), // 10 minutes ago
        latency_ms: 3400,
        user_id: 'user_002'
      },
      {
        id: 3,
        workflow_run_id: 'wf_34567890-3456-7890-bcde-345678901234',
        conversation_id: 'conv_65432109-2109-6543-ba98-765432109876',
        input_text: 'Translate this text to French',
        output_text: 'This translation is in progress...',
        status: 'running',
        created_at: new Date(Date.now() - 1000 * 60 * 2).toISOString(), // 2 minutes ago
        latency_ms: null,
        user_id: 'user_003'
      },
      {
        id: 4,
        workflow_run_id: 'wf_45678901-4567-8901-cdef-456789012345',
        conversation_id: 'conv_54321098-1098-5432-a987-654321098765',
        input_text: 'Create a marketing plan',
        output_text: 'Here is a comprehensive marketing plan...',
        status: 'success',
        created_at: new Date(Date.now() - 1000 * 60 * 15).toISOString(), // 15 minutes ago
        latency_ms: 2100,
        user_id: 'user_001'
      },
      {
        id: 5,
        workflow_run_id: 'wf_56789012-5678-9012-def0-567890123456',
        conversation_id: 'conv_43210987-0987-4321-9876-543210987654',
        input_text: 'Analyze customer feedback data',
        output_text: 'Based on the analysis of customer feedback...',
        status: 'completed',
        created_at: new Date(Date.now() - 1000 * 60 * 30).toISOString(), // 30 minutes ago
        latency_ms: 1800,
        user_id: 'user_004'
      }
    ]

    return NextResponse.json({
      success: true,
      logs: mockLogs,
      total: mockLogs.length,
      source: 'Mock Data (Backend unavailable)'
    })
  }
}
