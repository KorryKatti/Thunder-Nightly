package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os/exec"
	"regexp"
	"runtime"
	"strings"
)

// App struct
type App struct {
	ctx context.Context
}

// RepoInfo holds GitHub repository metadata
type RepoInfo struct {
	Name          string
	FullName      string
	Description   string
	Stars         int
	Forks         int
	Language      string
	LicenseName   string
	URL           string
	DefaultBranch string
	OpenIssues    int
	Watchers      int
}

// RepoLicense holds license info
type RepoLicense struct {
	Name string `json:"name"`
}

// GitHubRepo is the raw API response
type GitHubRepo struct {
	Name            string      `json:"name"`
	FullName        string      `json:"full_name"`
	Description     string      `json:"description"`
	StargazersCount int         `json:"stargazers_count"`
	ForksCount      int         `json:"forks_count"`
	Language        string      `json:"language"`
	License         *RepoLicense `json:"license"`
	HTMLURL         string      `json:"html_url"`
	DefaultBranch   string      `json:"default_branch"`
	OpenIssuesCount int         `json:"open_issues_count"`
	SubscribersCount int        `json:"subscribers_count"`
}

// NewApp creates a new App application struct
func NewApp() *App {
	return &App{}
}

// startup is called when the app starts
func (a *App) startup(ctx context.Context) {
	a.ctx = ctx
}

// OpenExternal opens a URL in the system's default browser
func (a *App) OpenExternal(url string) error {
	var cmd *exec.Cmd
	switch runtime.GOOS {
	case "darwin":
		cmd = exec.Command("open", url)
	case "windows":
		cmd = exec.Command("rundll32", "url.dll,FileProtocolHandler", url)
	default:
		cmd = exec.Command("xdg-open", url)
	}
	return cmd.Start()
}

// CheckUVInstalled checks if uv is available in PATH
func (a *App) CheckUVInstalled() bool {
	_, err := exec.LookPath("uv")
	return err == nil
}

// GetUVVersion returns the installed uv version, or empty string
func (a *App) GetUVVersion() string {
	out, err := exec.Command("uv", "--version").Output()
	if err != nil {
		return ""
	}
	return strings.TrimSpace(string(out))
}

// InstallUV runs the official uv installer script
func (a *App) InstallUV() (string, error) {
	out, err := exec.Command("sh", "-c", "curl -LsSf https://astral.sh/uv/install.sh | sh").CombinedOutput()
	if err != nil {
		return string(out), fmt.Errorf("uv install failed: %w", err)
	}
	return string(out), nil
}

// parseGitHubURL extracts owner/repo from various GitHub URL formats
func parseGitHubURL(url string) (owner, repo string, err error) {
	url = strings.TrimSpace(url)
	url = strings.TrimSuffix(url, "/")
	url = strings.TrimSuffix(url, ".git")

	// Handle different URL formats
	patterns := []*regexp.Regexp{
		regexp.MustCompile(`github\.com/([^/]+)/([^/]+)`),
		regexp.MustCompile(`^([^/]+)/([^/]+)$`),
	}

	for _, p := range patterns {
		matches := p.FindStringSubmatch(url)
		if matches != nil {
			return matches[1], matches[2], nil
		}
	}

	return "", "", fmt.Errorf("invalid GitHub URL: %s", url)
}

// GetRepoInfo fetches repository information from GitHub API
func (a *App) GetRepoInfo(url string) (*RepoInfo, error) {
	log.Printf("GetRepoInfo called with URL: %s", url)

	owner, repo, err := parseGitHubURL(url)
	if err != nil {
		log.Printf("parseGitHubURL error: %v", err)
		return nil, err
	}
	log.Printf("Parsed owner=%s repo=%s", owner, repo)

	apiURL := fmt.Sprintf("https://api.github.com/repos/%s/%s", owner, repo)

	req, err := http.NewRequest("GET", apiURL, nil)
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %w", err)
	}
	req.Header.Set("Accept", "application/vnd.github.v3+json")
	req.Header.Set("User-Agent", "thunder-nightly")

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("failed to fetch repo: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode == 404 {
		return nil, fmt.Errorf("repository not found: %s/%s", owner, repo)
	}
	if resp.StatusCode != 200 {
		return nil, fmt.Errorf("GitHub API error: %d", resp.StatusCode)
	}

	var ghRepo GitHubRepo
	if err := json.NewDecoder(resp.Body).Decode(&ghRepo); err != nil {
		log.Printf("JSON decode error: %v", err)
		return nil, fmt.Errorf("failed to decode response: %w", err)
	}

	licenseName := ""
	if ghRepo.License != nil {
		licenseName = ghRepo.License.Name
	}

	result := &RepoInfo{
		Name:          ghRepo.Name,
		FullName:      ghRepo.FullName,
		Description:   ghRepo.Description,
		Stars:         ghRepo.StargazersCount,
		Forks:         ghRepo.ForksCount,
		Language:      ghRepo.Language,
		LicenseName:   licenseName,
		URL:           ghRepo.HTMLURL,
		DefaultBranch: ghRepo.DefaultBranch,
		OpenIssues:    ghRepo.OpenIssuesCount,
		Watchers:      ghRepo.SubscribersCount,
	}
	log.Printf("Returning repo info: %+v", result)
	return result, nil
}

// GetReadme fetches the README content from a GitHub repository
func (a *App) GetReadme(url string) (string, error) {
	owner, repo, err := parseGitHubURL(url)
	if err != nil {
		return "", err
	}

	apiURL := fmt.Sprintf("https://api.github.com/repos/%s/%s/readme", owner, repo)

	req, err := http.NewRequest("GET", apiURL, nil)
	if err != nil {
		return "", fmt.Errorf("failed to create request: %w", err)
	}
	req.Header.Set("Accept", "application/vnd.github.v3.raw")
	req.Header.Set("User-Agent", "thunder-nightly")

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return "", fmt.Errorf("failed to fetch README: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return "", fmt.Errorf("README not found (status %d)", resp.StatusCode)
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", fmt.Errorf("failed to read README: %w", err)
	}

	return string(body), nil
}

// InstallApp installs a Python app using uv
func (a *App) InstallApp(url string) (string, error) {
	owner, repo, err := parseGitHubURL(url)
	if err != nil {
		return "", err
	}

	// Clone and install using uv
	cloneURL := fmt.Sprintf("https://github.com/%s/%s.git", owner, repo)
	cmd := fmt.Sprintf("cd /tmp && rm -rf %s && git clone %s && cd %s && uv sync 2>&1", repo, cloneURL, repo)

	out, err := exec.Command("sh", "-c", cmd).CombinedOutput()
	if err != nil {
		return string(out), fmt.Errorf("install failed: %w", err)
	}

	return string(out), nil
}
