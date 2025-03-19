import { useQuery } from "@tanstack/react-query"
import { useState } from "react"
import { Button, Form, Input, Label, Spinner } from "reactstrap"
import axios from "axios"

// import mock_data from "../mock_data/result.txt"
import { IUserStatistics } from "../types"
import { Navigate } from "react-router"

const client = axios.create({
  baseURL: import.meta.env.VITE_GIT_RANK_API_URL,
  headers: {
    "Content-type": "application/json",
  },
})


export default function Root() {
  const [username, setUsername] = useState('')
  const [shouldFetch, setShouldFetch] = useState(false)

  const { isLoading, isError, isSuccess, data, error }= useQuery({
    queryKey: ['status', username],
    queryFn: async () => {
      const response = await client.get(`/rank/${username}`)
      setShouldFetch(false)
      return response.data as IUserStatistics
      // mock data fetching
      //return fetch(mock_data).then(r => r.json()).then(r => r as IUserStatistics)
    },
    enabled: shouldFetch,
    refetchOnWindowFocus: false,
    staleTime: 1000 * 60 * 10, // 10 minutes
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setShouldFetch(true)
  }

  return (
    <div>
    <h1 className="text-center">Git Rank</h1>
    <Form onSubmit={handleSubmit} className="input-form">
        <Label htmlFor="username">
          Username:
        </Label>
        <Input
          id="username"
          type="text"
          required
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

      <Button 
        type="submit"
        disabled={isLoading}
        color="primary"
      >
        {isLoading ? "Generating report..." : 'Generate report'}
      </Button>
      {isLoading && <Spinner color="primary" size="sm"/>}
    </Form>

    {isSuccess && (
      <Navigate to={`/report/${username}`} state={ data }></Navigate>
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
