import { IFileStatistics } from "../types";

export default function FileOverview({ fileStatistics }: {fileStatistics: IFileStatistics}) {
    return (
        <div>
        <p>Change type: {fileStatistics.file_state}</p>
        <p>Lint score: {fileStatistics.lint_score}</p>
        <p>Technology: {fileStatistics.technology}</p>
    </div>
    )
}
