import { IUserStatistics } from "../types";
import RepositoryOverview from "./RepositoryOverview";

export default function UserOverview({ userStatistics }: {userStatistics: IUserStatistics}) {
    return (
        <div>
            <h1>Report for user {userStatistics.username}</h1>
            <p>Total repositories: <b>{userStatistics.repositories.length}</b></p>
            {userStatistics.cross_repository &&
                <RepositoryOverview key={userStatistics.cross_repository.repository_name} repositoryStatistics={userStatistics.cross_repository}/>
            }
            {userStatistics.repositories.map(repository => (
                <RepositoryOverview key={repository.repository_name} repositoryStatistics={repository} />
            ))}
        </div>
    )
}