import {AccordionBody, AccordionHeader, AccordionItem, Button, Table, UncontrolledAccordion, UncontrolledCollapse } from "reactstrap"
import { IRepositoryStatistics } from "../types";
import TechnologyOverview from "./TechnologyOverview";
import CommitOverview from "./CommitOverview";
import TechnologiesBarChart from "./charts/TechnologiesBarChart";
import CommitsDateChart from "./charts/TechnologiesDateChart";
import LintScoreDateChart from "./charts/LintScoreDateChart";
import stringHash from "string-hash";


export default function RepositoryOverview({ repositoryStatistics }: {repositoryStatistics: IRepositoryStatistics}) {
    return (
        <>
            <h2 className="mt-4">Repository {repositoryStatistics.repository_name}</h2>
            {repositoryStatistics.commits.length != 0 && <div><Table size="sm" striped>
                <thead>
                    <tr>
                        <th>Technology</th>
                        <th>Total file changes</th>
                        <th>First used date</th>
                        <th>Last used date</th>
                        <th>Weeks used</th>
                    </tr>
                </thead>
                <tbody>
                {repositoryStatistics.technologies.map(technology => (
                    <TechnologyOverview key={technology.technology} technologyStatistics={technology}/>
                ))}
                </tbody>
            </Table>
            <div className="charts">
                <TechnologiesBarChart technologies={repositoryStatistics.technologies}/>
                <CommitsDateChart commits={repositoryStatistics.commits}/>
                <LintScoreDateChart commits={repositoryStatistics.commits}/>
            </div></div>}
            <h3>Commits</h3>
            <p>Total commits: <b>{repositoryStatistics.total_commits}</b></p>
            <p>User commits: <b>{repositoryStatistics.user_commits}</b></p>
            {repositoryStatistics.commits.length != 0 && <div><Button color="secondary" id={"commit_toggler".concat(stringHash(repositoryStatistics.repository_name).toString())}>Collapse user commits</Button>
            <UncontrolledCollapse toggler={"#commit_toggler".concat(stringHash(repositoryStatistics.repository_name).toString())}>
                {/* https://github.com/reactstrap/reactstrap/issues/2785 */}
                {/* @ts-expect-error Known Reactstrap issue */}
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
            </UncontrolledCollapse>
            </div>}
            <hr/>
        </>
    )
}
