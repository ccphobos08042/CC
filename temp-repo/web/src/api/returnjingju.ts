import { get, post } from '/@/utils/http/axios';
enum URL {
    list = '/myapp/admin/returnjingju/list',
    create = '/myapp/admin/returnjingju/create',
    update = '/myapp/admin/returnjingju/update',
    delete = '/myapp/admin/returnjingju/delete',

}

const listApi = async (params: any) => get<any>({ url: URL.list, params: params, data: {}, headers: {} });
const createApi = async (data: any) =>
    post<any>({ url: URL.create, params: {}, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
const updateApi = async (params: any, data: any) =>
    post<any>({ url: URL.update, params: params, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
const deleteApi = async (params: any) => post<any>({ url: URL.delete, params: params, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });

export { listApi, createApi, updateApi, deleteApi, };
