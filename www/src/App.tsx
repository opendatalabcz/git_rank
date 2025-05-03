import {QueryClient, QueryClientProvider} from '@tanstack/react-query'
import {
  createBrowserRouter,
  isRouteErrorResponse,
  RouterProvider,
  useNavigate,
  useRouteError
} from "react-router-dom"
import Root from "./routes/root"
import Report from "./routes/report"
import { Button, Container } from 'reactstrap'

function ErrorBoundary() {
  const navigate = useNavigate()
  const error = useRouteError()
  console.error(error)

  if(isRouteErrorResponse(error)) {
    return (  
      <Container className="px-2 py-3 text-center">
        <h1>HTTP {error.status}</h1>
        <p>{error.data}</p>
        <Button color="primary" onClick={() => navigate('/')}>Back to homepage</Button>
      </Container>
    )
  }
}

const queryClient = new QueryClient()

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root/>,
    errorElement: <ErrorBoundary />,
  },
  {
    path: "report/:username",
    element: <Report/>,
    errorElement: <ErrorBoundary />,
  }
])

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  )
}
