export interface HealthResponse {
    success: boolean;
    data: {
        status: string;
        message: string;
    };
}

export const checkBackendHealth = async (): Promise<HealthResponse> => {
    return {
        success: true,
        data: {
            status: 'ok',
            message: 'Frontend is running independently'
        }
    };
};