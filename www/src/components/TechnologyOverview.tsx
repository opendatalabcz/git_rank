import dayjs from "dayjs"
import { ITechnologyStatistics } from "../types"
import { DATE_FORMAT } from "../consts"

export default function TechnologyOverview({ technologyStatistics }: { technologyStatistics: ITechnologyStatistics }) {
    return (
        <tr>
            <td>{technologyStatistics.technology}</td>
            <td>{technologyStatistics.total_changes}</td>
            <td>{dayjs(technologyStatistics.first_used_date).format(DATE_FORMAT)}</td>
            <td>{dayjs(technologyStatistics.last_used_date).format(DATE_FORMAT)}</td>
            <td>{technologyStatistics.weeks_used}</td>
        </tr>
    )
}