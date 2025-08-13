#!/usr/bin/env python3

from github_integration_simple import GitHubIntegrationSimple

def test_simple_integration():
    """Test the simplified GitHub integration"""
    print("🤖 Testing Simplified GitHub Integration")
    print("=" * 50)
    
    # Initialize GitHub integration
    github_integration = GitHubIntegrationSimple()
    
    # Test repository analysis
    print("\n📋 Testing Repository Analysis:")
    proposals = github_integration.analyze_repository()
    
    print(f"✅ Generated {len(proposals)} issue proposals")
    
    for proposal in proposals:
        print(f"   - {proposal.title} ({proposal.severity})")
    
    # Test issue creation (if authenticated)
    if github_integration.headers:
        print("\n📝 Testing Issue Creation:")
        test_issue = github_integration.create_issue(
            title="Test Issue from Atim AI Assistant",
            body="This is a test issue created by the Atim AI Assistant to verify GitHub integration.",
            labels=["test", "automation"]
        )
        
        if "error" not in test_issue:
            print(f"✅ Test issue created successfully: #{test_issue['number']}")
        else:
            print(f"❌ Failed to create test issue: {test_issue['error']}")
    else:
        print("\n⚠️  GitHub App not authenticated - skipping issue creation test")
    
    print(f"\n🎉 Simplified GitHub integration test completed!")

if __name__ == "__main__":
    test_simple_integration()

