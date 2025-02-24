import {AccordionBody, AccordionHeader, AccordionItem, Table, UncontrolledAccordion } from "reactstrap"
import { IRepositoryStatistics } from "../types";
import TechnologyOverview from "./TechnologyOverview";
import CommitOverview from "./CommitOverview";
import TechnologiesPieChart from "./charts/TechnologiesPieChart";
import CommitsDateChart from "./charts/TechnologiesDateChart";
import LintScoreDateChart from "./charts/LintScoreDateChart";


export default function RepositoryOverview({ repositoryStatistics }: {repositoryStatistics: IRepositoryStatistics}) {
    return (
        <>
            <h2>Repository {repositoryStatistics.repository_name}</h2>
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
            <div className="charts">
            <TechnologiesPieChart technologies={repositoryStatistics.technologies}/>
            <CommitsDateChart commits={repositoryStatistics.commits}/>
            <LintScoreDateChart commits={repositoryStatistics.commits}/>
            </div>
            <h3>Commits</h3>
            <p>Total commits: {repositoryStatistics.total_commits}</p>
            <p>User commits: {repositoryStatistics.user_commits}</p>
            <UncontrolledAccordion stayOpen>
                {repositoryStatistics.commits.map(commit => (
                    <AccordionItem key={commit.commit_sha}>
                        <AccordionHeader targetId={commit.commit_sha}>
                            <b>Commit {commit.commit_sha}</b>
                        </AccordionHeader>
                        <AccordionBody accordionId={commit.commit_sha}>
                            <CommitOverview commitStatistics={commit}/>
                        </AccordionBody>
                    </AccordionItem>
                ))}
            </UncontrolledAccordion>
        </>
    )
}
