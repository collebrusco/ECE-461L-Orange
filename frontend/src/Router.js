import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
  RouterProvider,
  Navigate,
} from "react-router-dom";
import UserManagement from "./pages/UserManagement";
import ResourceManagement from "./pages/ResourceManagement";
import { RequireAuth } from "./components/AuthProvider";

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route>
      <Route index path="user" element={
        <RequireAuth>
          <UserManagement />
        </RequireAuth>
      }/>
      <Route path="resource" element={
        <RequireAuth>
          <ResourceManagement />
        </RequireAuth>
      }/>
      <Route path="*" element={<Navigate to="user" replace />} />
    </Route>
  )
);

function Router() {
  return <RouterProvider router={router} />;
}

export default Router;
