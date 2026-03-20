import { get, post } from '/@/utils/http/axios';
enum URL {
    list = '/myapp/admin/jingju/list',
    create = '/myapp/admin/jingju/create',
    update = '/myapp/admin/jingju/update',
    delete = '/myapp/admin/jingju/delete',
    yolo_v8 = '/myapp/admin/jingju/yolov8',
    opendoor='/myapp/admin/jingju/opendoor',

    baoxiu='/myapp/admin/baoxiu/create',
    returnjingjucreate='/myapp/admin/returnjingju/create',

}

const listApi = async (params: any) => get<any>({ url: URL.list, params: params,  headers: {} });
const createApi = async (data: any) =>
    post<any>({ url: URL.create, params: {}, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
const updateApi = async (params: any, data: any) =>
    post<any>({ url: URL.update, params: params, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
const deleteApi = async (params: any) => post<any>({ url: URL.delete, params: params, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
const yolov8Api = async (data: any) =>
    post<any>({ url: URL.yolo_v8, params: {}, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
const opendoorApi = async (params: any) => post<any>({ url: URL.opendoor, params: params, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
const baoxiuApi=async (data: any) =>
    post<any>({ url: URL.baoxiu, params: {}, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
const returnjingjucreateApi = async (data: any) =>
    post<any>({ url: URL.returnjingjucreate, params: {}, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });

export { listApi, createApi, updateApi, deleteApi, yolov8Api,opendoorApi,baoxiuApi,returnjingjucreateApi};
