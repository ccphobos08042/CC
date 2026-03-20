import { get, post } from '/@/utils/http/axios';
enum URL {
    list = '/myapp/admin/courseinfo/list',
    create = '/myapp/admin/courseinfo/create',
    update = '/myapp/admin/courseinfo/update',
    delete = '/myapp/admin/courseinfo/delete',
}
// ... existing code ...
/*enum URL {
    list = 'https://127.0.0.0:8000/myapp/admin/courseinfo/list',
    create = 'https://127.0.0.0:8000/myapp/admin/courseinfo/create',
    update = 'https://127.0.0.0:8000/myapp/admin/courseinfo/update',
    delete = 'https://127.0.0.0:8000/myapp/admin/courseinfo/delete',
}*/
// ... existing code ...


const listApi = async (params: any) => get<any>({ url: URL.list, params: params, data: {}, headers: {} });
const createApi = async (data: any) =>
    post<any>({ url: URL.create, params: {}, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
const updateApi = async (params: any, data: any) =>
    post<any>({ url: URL.update, params: params, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
const deleteApi = async (params: any) => post<any>({ url: URL.delete, params: params, headers: {} });

export { listApi, createApi, updateApi, deleteApi };
