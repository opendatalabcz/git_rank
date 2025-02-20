import {QueryClient, QueryClientProvider} from '@tanstack/react-query'
import {
  createBrowserRouter,
  RouterProvider
} from "react-router-dom";
import Report from "./routes/report"

const queryClient = new QueryClient()

const router = createBrowserRouter([
  {
    path: "/",
    element: <Report/>
  }
])

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  )
}
