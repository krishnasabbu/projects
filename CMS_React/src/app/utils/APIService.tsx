import axios from 'axios';

interface ApiResponse<T> {
  data: T;
}

export const APIService = {
  async get<T>(url: string): Promise<T> {
    const response = await axios.get<T>(url);
    console.log("response === "+JSON.stringify(response.data));
    return response.data;
  },
  
  async post<T>(url: string, data: any): Promise<T> {
    const response = await axios.post<ApiResponse<T>>(url, data);
    return response.data.data;
  },
  // Add other HTTP methods as needed
};