// User related types
export interface User {
  id: string;
  email: string;
  verified: boolean;
}

// Github related types
export interface GithubIssue {
  id: number;
  number: number;
  title: string;
  state: string;
  html_url: string;
  created_at: string;
  updated_at: string;
  body: string;
  labels: GithubLabel[];
}

export interface GithubLabel {
  id: number;
  name: string;
  color: string;
}

export interface GithubPullRequest {
  id: number;
  number: number;
  title: string;
  state: string;
  html_url: string;
  created_at: string;
  updated_at: string;
  body: string;
  diff_url: string;
  head: {
    ref: string;
  };
  base: {
    ref: string;
  };
}

// Atim related types
export interface Issue {
  id: string;
  title: string;
  description: string;
  severity: "low" | "medium" | "high";
  status: "open" | "fixed" | "rejected";
  file_path: string;
  line_number: number;
  created_at: string;
  updated_at: string;
  suggested_fix?: string;
}

export interface PullRequest {
  id: string;
  github_id: number;
  title: string;
  description: string;
  status: "open" | "merged" | "closed";
  created_at: string;
  updated_at: string;
  diff?: string;
  html_url: string;
  feedback?: Feedback[];
}

export interface Feedback {
  id: string;
  pr_id: string;
  comment: string;
  approved: boolean;
  created_at: string;
}

export interface MeTTaProof {
  proof_id: string;
  theorem: string;
  premises: string[];
  conclusion: string;
  proof_steps: string[];
  confidence: number;
  reasoning_type: string;
  timestamp: string;
}

export interface MeTTaAnalysis {
  analysis_id: string;
  query: string;
  reasoning_type: string;
  formal_specification: string;
  proof?: MeTTaProof;
  response: string;
  confidence: number;
  metadata: Record<string, any>;
}

export interface ChatMessage {
  id: string;
  sender: "user" | "atim";
  content: string;
  timestamp: string;
  reference_id?: string; // ID of the issue or PR this message refers to
  reference_type?: "issue" | "pr";
  metadata?: {
    analysis_id?: string;
    reasoning_type?: string;
    confidence?: number;
    formal_specification?: string;
    proof_id?: string;
    theorem?: string;
  };
}

export interface KanbanItem {
  id: string;
  title: string;
  description: string;
  status: "todo" | "in-progress" | "done";
  type: "issue" | "pr";
  url: string;
  number: number;
  created_at: string;
  updated_at: string;
}

// API response types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}
