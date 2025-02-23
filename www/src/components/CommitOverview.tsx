import dayjs from "dayjs";
import { ICommitStatistics } from "../types";
import { DATE_FORMAT } from "../consts";
import { AccordionBody, AccordionHeader, AccordionItem, UncontrolledAccordion } from "reactstrap";
import FileOverview from "./FileOverview";

export default function CommitOverview({ commitStatistics }: { commitStatistics: ICommitStatistics}) {
    return (
        <div>
            <p>Average add lint score: {commitStatistics.average_add_lint_score}</p>
            <p>Average change lint score: {commitStatistics.average_change_lint_score}</p>
            <p>Committed: {dayjs(commitStatistics.commit_date).format(DATE_FORMAT)}</p>
            <h4>Files</h4>
            <UncontrolledAccordion stayOpen>
                {commitStatistics.files.map(file => (
                    <AccordionItem key={file.file_name}>
                        <AccordionHeader targetId={file.file_name}>
                            <b>File {file.file_name}</b>
                        </AccordionHeader>
                        <AccordionBody accordionId={file.file_name}>
                            <FileOverview fileStatistics={file}/>
                        </AccordionBody>
                    </AccordionItem>
                ))}
            </UncontrolledAccordion>
        </div>
    )
}
