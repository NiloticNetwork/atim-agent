#!/usr/bin/env python3

import os
import re
import json
import time
import requests
from datetime import datetime
from typing import List, Dict, Optional
from github import Github, GithubException
from dataclasses import dataclass, asdict

@dataclass
class IssueProposal:
    id: str
    title: str
    description: str
    severity: str  # 'low', 'medium', 'high', 'critical'
    category: str  # 'bug', 'enhancement', 'security', 'performance', 'documentation'
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    suggested_fix: Optional[str] = None
    labels: List[str] = None
    created_at: str = None
    status: str = 'pending'  # 'pending', 'approved', 'rejected', 'published'
    github_issue_number: Optional[int] = None
    
    def __post_init__(self):
        if self.labels is None:
            self.labels = []
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

class GitHubIntegration:
    def __init__(self, github_token: str = None, repo_name: str = "NiloticNetwork/NiloticNetworkBlockchain"):
        # Try to use Atim's bot token first, fallback to user token
        self.github_token = github_token or os.environ.get('ATIM_GITHUB_TOKEN')
        self.repo_name = repo_name
        self.g = Github(self.github_token) if self.github_token else None
        self.repo = None
        self.bot_mode = bool(os.environ.get('ATIM_GITHUB_TOKEN'))
        
        if self.g:
            try:
                self.repo = self.g.get_repo(repo_name)
                if self.bot_mode:
                    print(f"🤖 Atim bot accessing repository: {repo_name}")
                else:
                    print(f"👤 User accessing repository: {repo_name}")
            except GithubException as e:
                print(f"Error accessing repository {repo_name}: {e}")
    
    def analyze_repository(self) -> List[IssueProposal]:
        """Analyze the repository and generate issue proposals"""
        if not self.repo:
            return self._generate_sample_proposals()
        
        proposals = []
        
        # Analyze different aspects of the codebase
        proposals.extend(self._analyze_security_issues())
        proposals.extend(self._analyze_performance_issues())
        proposals.extend(self._analyze_code_quality_issues())
        proposals.extend(self._analyze_documentation_issues())
        proposals.extend(self._analyze_architecture_issues())
        
        return proposals
    
    def _analyze_security_issues(self) -> List[IssueProposal]:
        """Analyze potential security issues"""
        proposals = []
        
        # Check for common security patterns
        security_patterns = [
            {
                'pattern': r'strcpy\s*\(',
                'title': 'Use of unsafe strcpy function',
                'description': 'The code uses strcpy which is vulnerable to buffer overflows. Consider using strncpy or std::string.',
                'severity': 'high',
                'category': 'security',
                'labels': ['security', 'bug']
            },
            {
                'pattern': r'sprintf\s*\(',
                'title': 'Use of unsafe sprintf function',
                'description': 'sprintf is vulnerable to buffer overflows. Use snprintf or std::string formatting.',
                'severity': 'high',
                'category': 'security',
                'labels': ['security', 'bug']
            },
            {
                'pattern': r'rand\s*\(',
                'title': 'Use of predictable random number generation',
                'description': 'rand() is not cryptographically secure. Use std::random_device or crypto-secure RNG for cryptographic operations.',
                'severity': 'medium',
                'category': 'security',
                'labels': ['security', 'enhancement']
            }
        ]
        
        try:
            contents = self.repo.get_contents("")
            for content_file in contents:
                if content_file.type == "file" and content_file.path.endswith(('.cpp', '.c', '.h', '.hpp')):
                    try:
                        file_content = content_file.decoded_content.decode('utf-8')
                        for pattern_info in security_patterns:
                            if re.search(pattern_info['pattern'], file_content):
                                proposals.append(IssueProposal(
                                    id=f"sec_{len(proposals) + 1}",
                                    title=pattern_info['title'],
                                    description=pattern_info['description'],
                                    severity=pattern_info['severity'],
                                    category=pattern_info['category'],
                                    file_path=content_file.path,
                                    labels=pattern_info['labels']
                                ))
                    except Exception as e:
                        print(f"Error analyzing file {content_file.path}: {e}")
        except Exception as e:
            print(f"Error accessing repository contents: {e}")
        
        return proposals
    
    def _analyze_performance_issues(self) -> List[IssueProposal]:
        """Analyze potential performance issues"""
        proposals = []
        
        performance_patterns = [
            {
                'pattern': r'std::vector.*\.push_back\s*\(',
                'title': 'Inefficient vector operations',
                'description': 'Consider reserving vector capacity before multiple push_back operations to avoid reallocations.',
                'severity': 'medium',
                'category': 'performance',
                'labels': ['performance', 'enhancement']
            },
            {
                'pattern': r'std::string.*\+.*std::string',
                'title': 'Inefficient string concatenation',
                'description': 'String concatenation with + operator creates temporary objects. Consider using std::stringstream or reserve() for better performance.',
                'severity': 'low',
                'category': 'performance',
                'labels': ['performance', 'enhancement']
            }
        ]
        
        # Add performance analysis logic here
        return proposals
    
    def _analyze_code_quality_issues(self) -> List[IssueProposal]:
        """Analyze code quality issues"""
        proposals = []
        
        quality_patterns = [
            {
                'pattern': r'using namespace std;',
                'title': 'Avoid using namespace std in headers',
                'description': 'Using namespace std in headers can cause naming conflicts. Use specific using declarations or namespace qualifiers.',
                'severity': 'medium',
                'category': 'enhancement',
                'labels': ['code-quality', 'enhancement']
            },
            {
                'pattern': r'#define\s+[A-Z_]+',
                'title': 'Consider using const instead of #define',
                'description': 'Prefer const variables over #define for better type safety and debugging support.',
                'severity': 'low',
                'category': 'enhancement',
                'labels': ['code-quality', 'enhancement']
            }
        ]
        
        return proposals
    
    def _analyze_documentation_issues(self) -> List[IssueProposal]:
        """Analyze documentation issues"""
        proposals = []
        
        # Check for missing documentation
        proposals.append(IssueProposal(
            id="doc_1",
            title="Add comprehensive API documentation",
            description="The blockchain API lacks comprehensive documentation. Consider adding detailed API docs with examples.",
            severity="medium",
            category="documentation",
            labels=["documentation", "enhancement"]
        ))
        
        proposals.append(IssueProposal(
            id="doc_2",
            title="Add inline code documentation",
            description="Many functions lack inline documentation. Add Doxygen-style comments for better code maintainability.",
            severity="low",
            category="documentation",
            labels=["documentation", "enhancement"]
        ))
        
        return proposals
    
    def _analyze_architecture_issues(self) -> List[IssueProposal]:
        """Analyze architectural issues"""
        proposals = []
        
        # Based on the repository structure analysis
        proposals.append(IssueProposal(
            id="arch_1",
            title="Implement proper error handling strategy",
            description="The codebase needs a consistent error handling strategy. Consider implementing custom exception classes and error codes.",
            severity="medium",
            category="enhancement",
            labels=["architecture", "enhancement"]
        ))
        
        proposals.append(IssueProposal(
            id="arch_2",
            title="Add comprehensive logging system",
            description="Implement a structured logging system for better debugging and monitoring of the blockchain application.",
            severity="medium",
            category="enhancement",
            labels=["architecture", "enhancement"]
        ))
        
        return proposals
    
    def _generate_sample_proposals(self) -> List[IssueProposal]:
        """Generate sample issue proposals when GitHub is not available"""
        return [
            IssueProposal(
                id="sample_1",
                title="Implement proper memory management in blockchain core",
                description="The blockchain core needs better memory management to prevent memory leaks in long-running operations.",
                severity="high",
                category="bug",
                file_path="src/core/blockchain.cpp",
                line_number=156,
                suggested_fix="Use smart pointers (std::unique_ptr, std::shared_ptr) instead of raw pointers",
                labels=["memory", "bug", "core"]
            ),
            IssueProposal(
                id="sample_2",
                title="Add input validation for transaction amounts",
                description="Transaction amounts should be validated to prevent negative or zero amounts.",
                severity="medium",
                category="security",
                file_path="src/core/transaction.cpp",
                line_number=89,
                suggested_fix="Add validation: if (amount <= 0) throw InvalidTransactionException();",
                labels=["security", "validation", "transaction"]
            ),
            IssueProposal(
                id="sample_3",
                title="Optimize database queries for large blockchain",
                description="Database queries need optimization for handling large blockchain datasets efficiently.",
                severity="medium",
                category="performance",
                file_path="src/persistence/database.cpp",
                line_number=234,
                suggested_fix="Add database indexes and implement query optimization",
                labels=["performance", "database", "optimization"]
            ),
            IssueProposal(
                id="sample_4",
                title="Add comprehensive unit tests",
                description="The codebase lacks comprehensive unit tests. Add tests for all core functionality.",
                severity="medium",
                category="enhancement",
                file_path="tests/",
                suggested_fix="Implement unit tests using Google Test or Catch2 framework",
                labels=["testing", "enhancement", "quality"]
            ),
            IssueProposal(
                id="sample_5",
                title="Implement proper thread safety in staking mechanism",
                description="The staking mechanism needs proper thread safety to handle concurrent staking operations.",
                severity="high",
                category="bug",
                file_path="src/core/staking.cpp",
                line_number=67,
                suggested_fix="Add mutex locks around staking operations and use atomic operations where appropriate",
                labels=["threading", "bug", "staking"]
            )
        ]
    
    def create_github_issue(self, proposal: IssueProposal) -> Optional[int]:
        """Create a GitHub issue from an approved proposal"""
        if not self.repo:
            print(f"GitHub repository not available. Token: {'Set' if self.github_token else 'Not set'}")
            return None
        
        try:
            # Prepare issue body with Atim's signature
            body = f"""
{proposal.description}

**Analysis Details:**
- **Severity:** {proposal.severity}
- **Category:** {proposal.category}
- **Detected by:** Atim AI Assistant
- **Timestamp:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

"""
            
            if proposal.file_path:
                body += f"**File:** `{proposal.file_path}`\n"
            
            if proposal.line_number:
                body += f"**Line:** {proposal.line_number}\n"
            
            if proposal.suggested_fix:
                body += f"\n**Suggested Fix:**\n```cpp\n{proposal.suggested_fix}\n```\n"
            
            body += f"\n---\n🤖 *Generated by Atim AI Assistant*"
            
            if self.bot_mode:
                print(f"🤖 Atim creating issue: {proposal.title}")
            else:
                print(f"👤 User creating issue: {proposal.title}")
            
            print(f"Repository: {self.repo_name}")
            print(f"Labels: {proposal.labels}")
            
            # Create the issue
            issue = self.repo.create_issue(
                title=proposal.title,
                body=body,
                labels=proposal.labels
            )
            
            if self.bot_mode:
                print(f"🤖 Atim created issue: #{issue.number}")
            else:
                print(f"👤 User created issue: #{issue.number}")
            
            return issue.number
            
        except GithubException as e:
            print(f"GitHub API Error creating issue: {e}")
            print(f"Error type: {type(e)}")
            print(f"Error status: {getattr(e, 'status', 'unknown')}")
            return None
        except Exception as e:
            print(f"Unexpected error creating GitHub issue: {e}")
            return None
    
    def get_repository_stats(self) -> Dict:
        """Get repository statistics"""
        if not self.repo:
            return {
                'name': self.repo_name,
                'open_issues': 0,
                'open_pulls': 0,
                'stars': 0,
                'forks': 0,
                'language': 'C++'
            }
        
        try:
            return {
                'name': self.repo.full_name,
                'open_issues': self.repo.open_issues_count,
                'open_pulls': len(list(self.repo.get_pulls(state='open'))),
                'stars': self.repo.stargazers_count,
                'forks': self.repo.forks_count,
                'language': self.repo.language or 'C++'
            }
        except GithubException as e:
            print(f"Error getting repository stats: {e}")
            return {}

def create_github_integration() -> GitHubIntegration:
    """Create GitHub integration instance"""
    github_token = os.environ.get('GITHUB_TOKEN', '')
    return GitHubIntegration(github_token) 