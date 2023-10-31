import React from "react";
import {
  getUserProjects,
  createProject as createProjectApi,
  joinProject as joinProjectApi,
  getResources,
  checkout as checkoutApi,
  checkin as checkinApi,
} from "../lib/api";
import { useAuth } from "./AuthProvider";

const StoreContext = React.createContext(null);
export function useStore() {
  return React.useContext(StoreContext);
}

export default function StoreProvider({ children }) {
  const { user } = useAuth();

  const [projects, setProjects] = React.useState([]);
  const [resources, setResources] = React.useState([]);

  const updateProjects = () => getUserProjects().then(setProjects);
  const updateResources = () => getResources().then(setResources);

  React.useEffect(() => {
    updateProjects();
    updateResources();
  }, [user]);

  // Exported functions
  const createProject = (name, description) => {
    return createProjectApi(name, description).then(updateProjects);
  };
  const joinProject = (projectName) => {
    return joinProjectApi(projectName).then(updateProjects);
  };
  const checkout = (resource_name, quantity, project_name) => {
    return checkoutApi(resource_name, quantity, project_name).then(() => {
      updateProjects();
      updateResources();
    });
  };
  const checkin = (resource_name, quantity, project_name) => {
    return checkinApi(resource_name, quantity, project_name).then(() => {
      updateProjects();
      updateResources();
    });
  };

  return (
    <StoreContext.Provider
      value={{
        projects,
        resources,
        createProject,
        joinProject,
        checkout,
        checkin,
      }}
    >
      {children}
    </StoreContext.Provider>
  );
}
