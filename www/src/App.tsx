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
import { Button } from 'reactstrap'

function ErrorBoundary() {
  const navigate = useNavigate()
  const error = useRouteError()
  console.error(error)

  if(isRouteErrorResponse(error)) {
    return (  
      <div>
        <h2>HTTP {error.status}</h2>
        <p>{error.data}</p>
        <Button color="primary" onClick={() => navigate('/')}>Go to homepage</Button>
      </div>
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
