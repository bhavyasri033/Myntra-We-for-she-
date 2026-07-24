export const ROUTES = {
  HOME: '/',
  AUTH: '/auth',
  LOCATION_PERMISSION: '/location-permission',
  CHOOSE_CITY: '/choose-city',
  LOCATING: '/locating',
  NEARBY: '/nearby',
  EXPLORE: '/explore',
  STATE_DETAILS: '/state/:stateId',
  HUB_DETAILS: '/hub/:hubId',
  STORE_DETAILS: '/store/:storeId',
  COLLECTIONS: '/collections/:storeId',
  PRODUCT_DETAILS: '/product/:productId',
  SHORTLIST: '/shortlist',
  NOT_FOUND: '*',
};

export const getHubDetailsPath = (hubId) => `/hub/${hubId}`;
export const getStoreDetailsPath = (storeId) => `/store/${storeId}`;
export const getCollectionsPath = (storeId) => `/collections/${storeId}`;
export const getProductDetailsPath = (productId) => `/product/${productId}`;
export const getStateDetailsPath = (stateId) => `/state/${stateId}`;

export default ROUTES;
