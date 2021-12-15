export const selectModuleList = (state: any) => state.entities.modules;
export const clearModuleList = (state: any) => {
  if (typeof state.entities !== "undefined") {
    state.entities.modules.length = 0;
    console.log(state.entities.modules);
  }
};
export const selectModuleDefsList = (state: any) => state.entities.modules_defs;
