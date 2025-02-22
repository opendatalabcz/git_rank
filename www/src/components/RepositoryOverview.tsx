import { Table } from "reactstrap"
import { IRepositoryStatistics } from "../types";
import TechnologyOverview from "./TechnologyOverview";


export default function RepositoryOverview({ repositoryStatistics }: {repositoryStatistics: IRepositoryStatistics}) {
    return (
        <>
            <h2>Repository {repositoryStatistics.repository_name}</h2>
            <p>Total commits: {repositoryStatistics.total_commits}</p>
            <p>User commits: {repositoryStatistics.user_commits}</p>
            <h3>Technologies used</h3>
            <Table size="sm" striped>
                <thead>
                    <tr>
                        <th>Technology</th>
                        <th>Total changes</th>
                        <th>First used date</th>
                        <th>Last used date</th>
                    </tr>
                </thead>
                <tbody>
                {repositoryStatistics.technologies.map(technology => (
                    <TechnologyOverview key={technology.technology} technologyStatistics={technology}/>
                ))}
                </tbody>
            </Table>
        </>
    )
}