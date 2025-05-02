import { useQuery } from "@tanstack/react-query"
import { useState } from "react"
import { Alert, Button, Card, CardBody, CardImg, CardText, CardTitle, Container, Form, Input, Label, Spinner } from "reactstrap"
import axios from "axios"

import git_rank_report from "../assets/git_rank_report.jpg"
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
  const [repository, setRepository] = useState('')
  const [shouldFetch, setShouldFetch] = useState(false)

  const { isLoading, isError, isSuccess, data, error }= useQuery({
    queryKey: ['status', username, repository],
    queryFn: async () => {
      let response
      if (repository != '') {
        response = await client.get(`/rank/${username}/repository`, {
          params: {
            repository_url: repository
          }
        });
      }
      else {
        response = await client.get(`/rank/${username}`)
      }
      setShouldFetch(false)
      return response.data as IUserStatistics
    },
    enabled: shouldFetch,
    refetchOnWindowFocus: false,
    staleTime: 1000 * 60 * 10, // 10 minutes
    retry: false,
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setShouldFetch(true)
  }

  return (
  <Container fluid className="px-2 py-3">
    <h1 className="text-center">GitRank</h1>
    <Form onSubmit={handleSubmit} className="input-form">
        <Label htmlFor="username" className="input-form-label">
          Username:
        </Label>
        <Input
          id="username"
          type="text"
          required
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <Label htmlFor="repository" className="input-form-label">
          Repository URL (optional):
        </Label>
        <Input
          id="repository"
          type="url"
          value={repository}
          onChange={(e) => setRepository(e.target.value)}
        />
      <Button 
        type="submit"
        disabled={isLoading}
        color="primary"
        className="submit-button"
      >
        {isLoading ? "Generating report..." : 'Generate report'}
        {isLoading ? (<Spinner color="light" size="sm"/>) : null}
      </Button>
    </Form>

    {isSuccess && (
      <Navigate to={`/report/${username}`} state={ data }></Navigate>
    )}

    {isError && (
      <Alert color="danger">
        Error while getting report: {error.message}
        <br/>
        {error.stack}
      </Alert>
    )}
    <Card className="my-2 mt-4 text-center" color="light">
      <CardBody>
        <CardTitle tag="h2">
          Co je GitRank?
        </CardTitle>
        <CardText>
        <p>GitRank je software sloužící k analýze a hodnocení uživatelské práce ve veřejných repozitářích (aktuálně z platformy GitHub) a následnému zobrazování výsledných reportů.</p>
        <p>Poskytuje tak vhled na dovednosti a návyky vývojářů, které nemusí být na první pohled patrné.</p>
        <p>GitRank vznikl jako diplomová práce na Fakultě informačních technologií ČVUT ve spolupráci s OpenDataLab.</p>
        </CardText>
        <CardImg src={git_rank_report} style={{width: "70%"}}/>
      </CardBody>
    </Card>
  </Container>
  );
}
