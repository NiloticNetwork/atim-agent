import axios from "axios";
import {
  ApiResponse,
  ChatMessage,
  Feedback,
  Issue,
  KanbanItem,
  PullRequest,
  User,
} from "../types";

// Create an Axios instance with default config
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:5000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

// Add interceptor to include auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Authentication
export const registerUser = async (
  email: string,
  password: string
): Promise<ApiResponse<{ message: string }>> => {
  try {
    const response = await api.post<ApiResponse<{ message: string }>>(
      "/register",
      { email, password }
    );
    return response.data;
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : "Registration failed",
    };
  }
};

export const verifyEmail = async (
  token: string
): Promise<ApiResponse<{ message: string }>> => {
  try {
    const response = await api.get<ApiResponse<{ message: string }>>(
      `/verify?token=${token}`
    );
    return response.data;
  } catch (error) {
    return {
      success: false,
      error:
        error instanceof Error ? error.message : "Email verification failed",
    };
  }
};

export const loginUser = async (
  email: string,
  password: string
): Promise<ApiResponse<{ token: string; user: User }>> => {
  try {
    const response = await api.post<ApiResponse<{ token: string; user: User }>>(
      "/login",
      { email, password }
    );
    if (response.data.success && response.data.data?.token) {
      localStorage.setItem("token", response.data.data.token);
    }
    return response.data;
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : "Login failed",
    };
  }
};

export const logoutUser = (): void => {
  localStorage.removeItem("token");
};

export const getCurrentUser = async (): Promise<ApiResponse<User>> => {
  try {
    const response = await api.get<ApiResponse<User>>("/user");
    return response.data;
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : "Failed to get user data",
    };
  }
};

// Issues
export const getIssues = async (): Promise<ApiResponse<Issue[]>> => {
  try {
    const response = await api.get<ApiResponse<Issue[]>>("/demo/issues");
    return response.data;
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : "Failed to fetch issues",
    };
  }
};

export const getIssue = async (id: string): Promise<ApiResponse<Issue>> => {
  try {
    const response = await api.get<ApiResponse<Issue>>(`/issues/${id}`);
    return response.data;
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : "Failed to fetch issue",
    };
  }
};

// Pull Requests
export const getPullRequests = async (): Promise<
  ApiResponse<PullRequest[]>
> => {
  try {
    const response = await api.get<ApiResponse<PullRequest[]>>("/prs");
    return response.data;
  } catch (error) {
    return {
      success: false,
      error:
        error instanceof Error
          ? error.message
          : "Failed to fetch pull requests",
    };
  }
};

export const getPullRequest = async (
  id: string
): Promise<ApiResponse<PullRequest>> => {
  try {
    const response = await api.get<ApiResponse<PullRequest>>(`/prs/${id}`);
    return response.data;
  } catch (error) {
    return {
      success: false,
      error:
        error instanceof Error ? error.message : "Failed to fetch pull request",
    };
  }
};

export const submitFeedback = async (
  prId: string,
  comment: string,
  approved: boolean
): Promise<ApiResponse<Feedback>> => {
  try {
    const response = await api.post<ApiResponse<Feedback>>(
      `/prs/${prId}/feedback`,
      { comment, approved }
    );
    return response.data;
  } catch (error) {
    return {
      success: false,
      error:
        error instanceof Error ? error.message : "Failed to submit feedback",
    };
  }
};

// Chat
export const getChatMessages = async (
  referenceId?: string,
  referenceType?: "issue" | "pr"
): Promise<ApiResponse<ChatMessage[]>> => {
  try {
    let url = "/demo/chat";
    if (referenceId && referenceType) {
      url += `?referenceId=${referenceId}&referenceType=${referenceType}`;
    }
    const response = await api.get<ApiResponse<ChatMessage[]>>(url);
    return response.data;
  } catch (error) {
    return {
      success: false,
      error:
        error instanceof Error
          ? error.message
          : "Failed to fetch chat messages",
    };
  }
};

export const sendChatMessage = async (
  content: string,
  referenceId?: string,
  referenceType?: "issue" | "pr"
): Promise<ApiResponse<ChatMessage>> => {
  try {
    const response = await api.post<ApiResponse<ChatMessage>>("/demo/chat", {
      content,
      referenceId,
      referenceType,
    });
    return response.data;
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : "Failed to send message",
    };
  }
};

// Kanban
export const getKanbanItems = async (): Promise<ApiResponse<KanbanItem[]>> => {
  try {
    const response = await api.get<ApiResponse<KanbanItem[]>>("/kanban");
    return response.data;
  } catch (error) {
    return {
      success: false,
      error:
        error instanceof Error ? error.message : "Failed to fetch kanban items",
    };
  }
};

export default api;
