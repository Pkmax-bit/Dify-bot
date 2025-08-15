import { get, post, postPublic, getPublic } from './base'

export interface ChatRequest {
  query: string
  inputs?: Record<string, any>
  model_config: Record<string, any>
  response_mode: 'streaming' | 'blocking'
  conversation_id?: string
  parent_message_id?: string
  user: string
  files?: Array<{
    type: 'image' | 'document'
    transfer_method: 'remote_url' | 'local_file'
    url?: string
    upload_file_id?: string
  }>
}

export interface ChatResponse {
  message_id: string
  conversation_id: string
  mode: string
  answer: string
  metadata: {
    usage: {
      prompt_tokens: number
      completion_tokens: number
      total_tokens: number
    }
    retriever_resources: any[]
  }
  created_at: number
}

// For published apps - use site API
export interface PublishedChatRequest {
  query: string
  inputs?: Record<string, any>
  response_mode: 'streaming' | 'blocking'
  conversation_id?: string
  user: string
  files?: Array<{
    type: 'image' | 'document'
    transfer_method: 'remote_url' | 'local_file'
    url?: string
    upload_file_id?: string
  }>
}

export interface PublishedChatResponse {
  message_id: string
  conversation_id: string
  mode: string
  answer: string
  metadata: {
    usage: {
      prompt_tokens: number
      completion_tokens: number
      total_tokens: number
    }
    retriever_resources: any[]
  }
  created_at: number
}

// Chat history
export interface ChatMessage {
  id: string
  conversation_id: string
  query: string
  answer: string
  message_files?: any[]
  feedback: {
    rating: 'like' | 'dislike' | null
  } | null
  created_at: number
}

export interface ConversationListResponse {
  data: Array<{
    id: string
    name: string
    inputs: Record<string, any>
    status: string
    created_at: number
    updated_at: number
    message_count: number
  }>
  has_more: boolean
  limit: number
}

export interface MessagesListResponse {
  data: ChatMessage[]
  has_more: boolean
  limit: number
}

// Internal API for development/testing
export const sendChatMessage = async (appId: string, request: ChatRequest): Promise<ChatResponse> => {
  return post<ChatResponse>(`/apps/${appId}/chat-messages`, { body: request })
}

// Published app API - use site access token
export const sendPublishedChatMessage = async (
  accessToken: string, 
  request: PublishedChatRequest
): Promise<PublishedChatResponse> => {
  return postPublic<PublishedChatResponse>(`/chat-messages`, { 
    body: request,
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  }, { isPublicAPI: true })
}

// Published workflow API - for workflow apps
export const runPublishedWorkflow = async (
  accessToken: string, 
  request: any
): Promise<any> => {
  return postPublic<any>(`/workflows/run`, { 
    body: request,
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  }, { isPublicAPI: true })
}

// Get conversation list for published app
export const getConversationList = async (
  accessToken: string,
  params?: { page?: number; limit?: number }
): Promise<ConversationListResponse> => {
  return getPublic<ConversationListResponse>('/conversations', {
    params,
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  })
}

// Get messages in conversation
export const getConversationMessages = async (
  accessToken: string,
  conversationId: string,
  params?: { page?: number; limit?: number }
): Promise<MessagesListResponse> => {
  return getPublic<MessagesListResponse>(`/conversations/${conversationId}/messages`, {
    params,
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  })
}

// Feedback on message
export const updateMessageFeedback = async (
  accessToken: string,
  messageId: string,
  rating: 'like' | 'dislike' | null
): Promise<void> => {
  return post<void>(`/messages/${messageId}/feedbacks`, {
    body: { rating },
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  }, { isPublicAPI: true })
}

// For workflow apps
export interface WorkflowRunRequest {
  inputs: Record<string, any>
  response_mode: 'streaming' | 'blocking'
  user: string
  files?: Array<{
    type: 'image' | 'document'
    transfer_method: 'remote_url' | 'local_file'
    url?: string
    upload_file_id?: string
  }>
}

export interface WorkflowRunResponse {
  workflow_run_id: string
  task_id: string
  data: {
    id: string
    workflow_id: string
    status: 'running' | 'succeeded' | 'failed'
    outputs: Record<string, any>
    error?: string
    elapsed_time: number
    total_tokens: number
    created_at: number
  }
}

export const runWorkflow = async (appId: string, request: WorkflowRunRequest): Promise<WorkflowRunResponse> => {
  return post<WorkflowRunResponse>(`/apps/${appId}/workflow-runs`, { body: request })
}

// Get app review statistics
export const getAppReviewStats = async (accessToken: string) => {
  return get(`/statistics/daily-conversations`, {
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  }, { isPublicAPI: true })
}

// Get conversation analytics
export const getConversationAnalytics = async (accessToken: string, params: {
  start?: string
  end?: string
}) => {
  return get(`/analysis/average-session-interactions`, {
    params,
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  }, { isPublicAPI: true })
}

// Get message feedback statistics
export const getMessageFeedbackStats = async (accessToken: string, params: {
  start?: string
  end?: string
}) => {
  return get(`/analysis/user-satisfaction-rate`, {
    params,
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  }, { isPublicAPI: true })
}
