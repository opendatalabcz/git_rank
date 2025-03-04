import { IUserStatistics } from "../types"
import UserOverview from "../components/UserOverview"
import { useNavigate, useLocation, useParams } from "react-router"
import { Button } from "reactstrap"


export default function Report() {
  const { username } = useParams()
  const navigate = useNavigate()
  const location = useLocation()

  const reportData: IUserStatistics = location.state

  if(!reportData) {
    return (
      <div>
        <h1>Report for user {username} was not generated!</h1>
        <p>Please generate a report first.</p>
        <Button color="primary" onClick={() => navigate('/')}>Go to homepage</Button>
      </div>
    )
  }

  return (
    <div>
    <UserOverview key={username} userStatistics={reportData}/>
    <h1>Raw data</h1>
    <pre>{JSON.stringify(reportData, null, 2)}</pre>
  </div>
  );
}
