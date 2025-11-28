from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from loguru import logger
from typing import Dict, Any
from datetime import datetime

from app.core.database import get_db
from app.models.user_segamaid import UserSegamaid

router = APIRouter()

# Segamaid绑定请求模型
class BindSegamaidRequest(BaseModel):
    playerId: str
    segamaidToken: str

# Segamaid绑定响应模型
class BindSegamaidResponse(BaseModel):
    status: str
    message: str
    data: Dict[str, Any] = None

@router.post("/bind", response_model=BindSegamaidResponse)
def bind_segamaid(request: BindSegamaidRequest, db: Session = Depends(get_db)):
    """
    绑定Segamaid
    
    Args:
        request: 绑定请求，包含玩家ID和Segamaid Token
        db: 数据库会话
    
    Returns:
        绑定结果
    """
    logger.info(f"绑定Segamaid请求: playerId={request.playerId}")
    
    try:
        # 验证请求参数
        if not request.playerId or not request.segamaidToken:
            raise HTTPException(status_code=400, detail="玩家ID和Segamaid Token不能为空")
        
        # 检查玩家是否已经绑定
        existing_bind = db.query(UserSegamaid).filter(
            UserSegamaid.player_id == request.playerId
        ).first()
        
        if existing_bind:
            # 更新现有绑定
            existing_bind.segamaid_token = request.segamaidToken
            existing_bind.status = "bound"
            existing_bind.update_time = datetime.utcnow()
            existing_bind.is_active = True
            db.commit()
            db.refresh(existing_bind)
            
            # 构造返回结果
            bind_result = {
                "playerId": existing_bind.player_id,
                "segamaidId": existing_bind.segamaid_id,
                "bindTime": existing_bind.bind_time.isoformat() + "Z",
                "status": existing_bind.status
            }
            
            logger.info(f"Segamaid绑定更新成功: playerId={request.playerId}")
            
            return BindSegamaidResponse(
                status="success",
                message="Segamaid绑定更新成功",
                data=bind_result
            )
        else:
            # 创建新绑定
            new_bind = UserSegamaid(
                player_id=request.playerId,
                segamaid_id=f"segamaid_{request.playerId}",
                segamaid_token=request.segamaidToken,
                status="bound",
                bind_time=datetime.utcnow(),
                update_time=datetime.utcnow(),
                is_active=True
            )
            
            db.add(new_bind)
            db.commit()
            db.refresh(new_bind)
            
            # 构造返回结果
            bind_result = {
                "playerId": new_bind.player_id,
                "segamaidId": new_bind.segamaid_id,
                "bindTime": new_bind.bind_time.isoformat() + "Z",
                "status": new_bind.status
            }
            
            logger.info(f"Segamaid绑定成功: playerId={request.playerId}")
            
            return BindSegamaidResponse(
                status="success",
                message="Segamaid绑定成功",
                data=bind_result
            )
    
    except HTTPException as e:
        logger.error(f"Segamaid绑定失败: {e.detail}")
        raise e
    
    except Exception as e:
        logger.error(f"Segamaid绑定失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Segamaid绑定失败: {str(e)}")

@router.get("/status/{player_id}")
def get_segamaid_status(player_id: str, db: Session = Depends(get_db)):
    """
    获取Segamaid绑定状态
    
    Args:
        player_id: 玩家ID
        db: 数据库会话
    
    Returns:
        绑定状态
    """
    logger.info(f"获取Segamaid绑定状态: player_id={player_id}")
    
    try:
        # 验证请求参数
        if not player_id:
            raise HTTPException(status_code=400, detail="玩家ID不能为空")
        
        # 查询绑定状态
        bind_info = db.query(UserSegamaid).filter(
            UserSegamaid.player_id == player_id,
            UserSegamaid.is_active == True
        ).first()
        
        if bind_info:
            # 构造返回结果
            status_result = {
                "playerId": bind_info.player_id,
                "segamaidId": bind_info.segamaid_id,
                "bindTime": bind_info.bind_time.isoformat() + "Z",
                "status": bind_info.status
            }
            
            logger.info(f"获取Segamaid绑定状态成功: player_id={player_id}")
            
            return {
                "status": "success",
                "message": "获取Segamaid绑定状态成功",
                "data": status_result
            }
        else:
            logger.info(f"玩家未绑定Segamaid: player_id={player_id}")
            
            return {
                "status": "success",
                "message": "玩家未绑定Segamaid",
                "data": None
            }
    
    except HTTPException as e:
        logger.error(f"获取Segamaid绑定状态失败: {e.detail}")
        raise e
    
    except Exception as e:
        logger.error(f"获取Segamaid绑定状态失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取Segamaid绑定状态失败: {str(e)}")

@router.delete("/unbind/{player_id}")
def unbind_segamaid(player_id: str, db: Session = Depends(get_db)):
    """
    解绑Segamaid
    
    Args:
        player_id: 玩家ID
        db: 数据库会话
    
    Returns:
        解绑结果
    """
    logger.info(f"解绑Segamaid请求: player_id={player_id}")
    
    try:
        # 验证请求参数
        if not player_id:
            raise HTTPException(status_code=400, detail="玩家ID不能为空")
        
        # 查询绑定关系
        bind_info = db.query(UserSegamaid).filter(
            UserSegamaid.player_id == player_id,
            UserSegamaid.is_active == True
        ).first()
        
        if bind_info:
            # 解除绑定
            bind_info.status = "unbound"
            bind_info.update_time = datetime.utcnow()
            bind_info.is_active = False
            db.commit()
            
            logger.info(f"Segamaid解绑成功: player_id={player_id}")
            
            return {
                "status": "success",
                "message": "Segamaid解绑成功"
            }
        else:
            logger.info(f"玩家未绑定Segamaid: player_id={player_id}")
            
            return {
                "status": "success",
                "message": "玩家未绑定Segamaid"
            }
    
    except HTTPException as e:
        logger.error(f"Segamaid解绑失败: {e.detail}")
        raise e
    
    except Exception as e:
        logger.error(f"Segamaid解绑失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Segamaid解绑失败: {str(e)}")