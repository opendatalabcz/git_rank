export interface IUserStatistics {
    username: string
    repositories: IRepositoryStatistics[]
}

export interface IRepositoryStatistics {
    repository_name: string
    total_commits: number
    user_commits: number
    technologies: ITechnologyStatistics[]
    commits: ICommitStatistics[]
}

export interface ITechnologyStatistics {
    technology: string
    total_changes: number
    first_used_date: string
    last_used_date: string
    weeks_used: number
}

export interface ICommitStatistics {
    average_add_lint_score: number | null
    average_change_lint_score: number | null
    commit_sha: string
    commit_date: string
    files: IFileStatistics[]
}

export interface IFileStatistics {
    file_name: string
    lint_score: number
    file_state: string
    technology: string
}
