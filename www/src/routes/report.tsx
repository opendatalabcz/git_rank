import { useQuery } from "@tanstack/react-query"
import { useState } from "react"
import { Button, Form, Input, Label, Spinner } from "reactstrap"
import axios from "axios"

// import mock_data from "../mock_data/result.txt"
import { IUserStatistics } from "../types"
import UserOverview from "../components/UserOverview"

const client = axios.create({
  baseURL: import.meta.env.VITE_GIT_RANK_API_URL,
  headers: {
    "Content-type": "application/json",
  },
})


export default function Report() {
  const [username, setUsername] = useState('')
  const [shouldFetch, setShouldFetch] = useState(false)

  const { isLoading, isError, isSuccess, data, error }= useQuery({
    queryKey: ['status', username],
    queryFn: async () => {
      const response = await client.get(`/rank/${username}`)
      setShouldFetch(false)
      return response.data as IUserStatistics
      // mock data fetching
      // return fetch(mock_data).then(r => r.json()).then(r => r as IUserStatistics)
    },
    enabled: shouldFetch,
    refetchOnWindowFocus: false,
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setShouldFetch(true)
  }

  return (
    <div>
    <Form onSubmit={handleSubmit}>
        <Label htmlFor="username">
          Insert username:
        </Label>
        <Input
          id="username"
          type="text"
          className="form-control"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

      <Button 
        type="submit"
        className="btn btn-primary"
        disabled={isLoading}
        color="primary"
      >
        {isLoading ? "Generating report..." : 'Generate report'}
      </Button>
      {isLoading && <Spinner color="primary" size="sm"/>}
    </Form>

    {isSuccess && (
      <div>
        <UserOverview key={username} userStatistics={data}/>
        <h1>Raw data</h1>
        <pre>{JSON.stringify(data, null, 2)}</pre>
      </div>
    )}

    {isError && (
      <div>
        Error while getting report: {error.message}
        <br/>
        {error.stack}
      </div>
    )}
  </div>
  );
}
