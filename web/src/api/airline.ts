import { get, post } from '/@/utils/http/axios';
enum URL {
    list = '/myapp/admin/airline/list',
    create = '/myapp/admin/airline/create',
    update = '/myapp/admin/airline/update',
    delete = '/myapp/admin/airline/delete',
    import = '/myapp/admin/airline/import',
}

const listApi = async (params: any) => get<any>({ url: URL.list, params: params, data: {}, headers: {} });
const createApi = async (data: any) =>
    post<any>({ url: URL.create, params: {}, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
const updateApi = async (params: any, data: any) =>
    post<any>({ url: URL.update, params: params, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
const deleteApi = async (params: any) => post<any>({ url: URL.delete, params: params, headers: {} });
const importApi = async (data: any) =>
    post<any>({ url: URL.import, params: {}, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });

export { listApi, createApi, updateApi, deleteApi, importApi };
